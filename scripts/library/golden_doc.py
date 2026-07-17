
"""
Standardized Golden Doc Generator
Matches "Archive Logic" for fonts, headers, and colors.
"""
import re
from googleapiclient.discovery import build

def create_google_doc_formatted(docs_service, drive_service, title, content, folder_id, user_name, lead_full_name=None, existing_doc_id=None):
    """Create or Update formatted Google Doc with bolding and lists (Golden Standard)"""
    try:
        doc_id = existing_doc_id
        
        if doc_id:
            # UPDATE existing doc
            print(f"Updating existing Doc: {doc_id}")
            try:
                drive_service.files().update(fileId=doc_id, body={'name': title}).execute()
            except Exception as e:
                print(f"  Warning: Could not rename doc: {e}")
            
            # Clear existing content
            doc = docs_service.documents().get(documentId=doc_id).execute()
            end_index = doc.get('body', {}).get('content', [{}])[-1].get('endIndex', 1)
            if end_index > 2:
                docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': [{'deleteContentRange': {'range': {'startIndex': 1, 'endIndex': end_index - 1}}}]}).execute()
        else:
            # CREATE NEW doc
            print(f"Creating new Doc: {title}")
            doc = docs_service.documents().create(body={'title': title}).execute()
            doc_id = doc.get('documentId')
            
            # Move to folder & Permission
            file = drive_service.files().get(fileId=doc_id, fields='parents').execute()
            prev_parents = ",".join(file.get('parents', []))
            drive_service.files().update(fileId=doc_id, addParents=folder_id, removeParents=prev_parents).execute()
            drive_service.permissions().create(fileId=doc_id, body={'type': 'anyone', 'role': 'reader'}).execute()
        
        # 2. Insert New Content
        requests_body = []
        index = 1
        
        # Title and By Line
        requests_body.append({'insertText': {'location': {'index': index}, 'text': title + "\n"}})
        requests_body.append({
            'updateParagraphStyle': {
                'range': {'startIndex': index, 'endIndex': index + len(title)},
                'paragraphStyle': {'namedStyleType': 'TITLE'},
                'fields': 'namedStyleType'
            }
        })
        index += len(title) + 1
        
        by_name = lead_full_name if lead_full_name else user_name
        by_line = f"By {by_name}\n"
        requests_body.append({'insertText': {'location': {'index': index}, 'text': by_line}})
        requests_body.append({
            'updateParagraphStyle': {
                'range': {'startIndex': index, 'endIndex': index + len(by_line)},
                'paragraphStyle': {'namedStyleType': 'SUBTITLE'},
                'fields': 'namedStyleType'
            }
        })
        index += len(by_line)
        
        # Content Cleaning
        if "```markdown" in content: content = content.split("```markdown")[1].split("```")[0].strip()
        elif content.startswith("```") and content.count("```") >= 2: content = content.split("```")[1].split("```")[0].strip()
        
        lines = content.split('\n')
        
        # 0. SETUP PAGE STYLE (White Page)
        requests_body.append({
            'updateDocumentStyle': {
                'documentStyle': {
                    'background': {'color': {'color': {'rgbColor': {'red': 1, 'green': 1, 'blue': 1}}}},
                    'pageSize': {'width': {'magnitude': 612, 'unit': 'PT'}, 'height': {'magnitude': 792, 'unit': 'PT'}},
                    'marginTop': {'magnitude': 72, 'unit': 'PT'}, 'marginBottom': {'magnitude': 72, 'unit': 'PT'},
                    'marginLeft': {'magnitude': 72, 'unit': 'PT'}, 'marginRight': {'magnitude': 72, 'unit': 'PT'}
                },
                'fields': 'background,pageSize,marginTop,marginBottom,marginLeft,marginRight'
            }
        })

        for line in lines:
            if not line.strip():
                requests_body.append({'insertText': {'location': {'index': index}, 'text': "\n"}})
                index += 1
                continue
            
            # Remove Title Repeats
            if line.strip() == f"# {title}" or line.strip() == f"# {title.split(' - ')[0]} - {title.split(' - ')[-1]}":
                continue 

            # Handle Headers
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                clean_text = line.lstrip('#').strip() + "\n"
                
                # UPDATED STYLES: Matches "Latest" Doc
                if level == 1: style, font_size = 'HEADING_1', 20
                elif level == 2: style, font_size = 'HEADING_2', 14 # Reduced to 14pt
                elif level == 3: style, font_size = 'HEADING_3', 12
                else: style, font_size = 'HEADING_4', 11
                
                requests_body.append({'insertText': {'location': {'index': index}, 'text': clean_text}})
                requests_body.append({
                    'updateParagraphStyle': {
                        'range': {'startIndex': index, 'endIndex': index + len(clean_text) - 1},
                        'paragraphStyle': {'namedStyleType': style, 'spaceAbove': {'magnitude': 18, 'unit': 'PT'}, 'spaceBelow': {'magnitude': 6, 'unit': 'PT'}},
                        'fields': 'namedStyleType,spaceAbove,spaceBelow'
                    }
                })
                requests_body.append({
                    'updateTextStyle': {
                        'range': {'startIndex': index, 'endIndex': index + len(clean_text) - 1},
                        'textStyle': {
                            'fontSize': {'magnitude': font_size, 'unit': 'PT'},
                            'weightedFontFamily': {'fontFamily': 'Arial'},
                            'bold': True,
                            'foregroundColor': {'color': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}}
                        },
                        'fields': 'fontSize,weightedFontFamily,bold,foregroundColor'
                    }
                })
                index += len(clean_text)
                continue

            # Handle Normal Text (with bolding)
            line_start_index = index
            line_style_requests = []
            
            parts = re.split(r'(\*\*.*?\*\*)', line)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    text = part[2:-2]
                    requests_body.append({'insertText': {'location': {'index': index}, 'text': text}})
                    line_style_requests.append({
                        'updateTextStyle': {
                            'range': {'startIndex': index, 'endIndex': index + len(text)},
                            'textStyle': {'bold': True, 'fontSize': {'magnitude': 11, 'unit': 'PT'}, 'weightedFontFamily': {'fontFamily': 'Arial'}, 'foregroundColor': {'color': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}}},
                            'fields': 'bold,fontSize,weightedFontFamily,foregroundColor'
                        }
                    })
                    index += len(text)
                else:
                    if not part: continue
                    requests_body.append({'insertText': {'location': {'index': index}, 'text': part}})
                    line_style_requests.append({
                        'updateTextStyle': {
                            'range': {'startIndex': index, 'endIndex': index + len(part)},
                            'textStyle': {'bold': False, 'fontSize': {'magnitude': 11, 'unit': 'PT'}, 'weightedFontFamily': {'fontFamily': 'Arial'}, 'foregroundColor': {'color': {'rgbColor': {'red': 0, 'green': 0, 'blue': 0}}}}, # Updated to 11pt
                            'fields': 'bold,fontSize,weightedFontFamily,foregroundColor'
                        }
                    })
                    index += len(part)
            
            requests_body.append({'insertText': {'location': {'index': index}, 'text': "\n"}})
            index += 1
            
            # Apply NORMAL_TEXT style first
            requests_body.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': line_start_index, 'endIndex': index},
                    'paragraphStyle': {'namedStyleType': 'NORMAL_TEXT'},
                    'fields': 'namedStyleType'
                }
            })
            
            # Apply specific styles
            requests_body.extend(line_style_requests)
            
        docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests_body}).execute()
        return f"https://docs.google.com/document/d/{doc_id}"
    except Exception as e:
        print(f"Doc error: {e}")
        return "ERROR"
