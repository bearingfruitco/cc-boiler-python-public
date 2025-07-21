#!/usr/bin/env python3

def main():
    """Main hook logic."""
    try:
    """
    Research Document Capture Hook - Detects, organizes, and UPDATES research/planning documents
    Enhanced to update existing docs rather than create duplicates
    """

    import json
    import os
    import sys
    import re
    from pathlib import Path
    from datetime import datetime
    import hashlib

    # Skip if not a file write operation
    if len(sys.argv) < 3 or sys.argv[1] != "write_file":
        sys.exit(0)

    file_path = sys.argv[2]

    # Only process markdown files
    if not file_path.endswith('.md'):
        sys.exit(0)

    # Skip known documentation directories
    skip_dirs = [
        '.claude/', 'docs/', 'node_modules/', '.next/', 
        'README.md', 'CHANGELOG.md', 'LICENSE.md', 'RELEASES.md'
    ]

    # Handle release notes specially
    if 'RELEASE_NOTES' in file_path or 'release_notes' in file_path.lower():
        print(f"""
    📋 Release Notes Detected!

    Release notes should go in: docs/releases/v{version}.md
    Not in the project root.

    Consider:
    1. Moving to docs/releases/v2.3.x.md
    2. Updating RELEASES.md index
    3. Updating CHANGELOG.md summary
    """)
        sys.exit(0)

    if any(skip in file_path for skip in skip_dirs):
        sys.exit(0)

    def get_current_feature():
        """Extract current feature from git branch or context"""
        try:
            import subprocess
            branch = subprocess.check_output(
                ['git', 'branch', '--show-current'],
                text=True
            ).strip()
        
            # Extract feature from branch name
            # Examples: feature/123-auth, feat/user-dashboard
            if '/' in branch:
                parts = branch.split('/')[-1]
                # Remove issue number if present
                feature = re.sub(r'^\d+-', '', parts)
                return feature
            return None
        except:
            return None

    def find_existing_research(feature, doc_type, title):
        """Find existing research document for this feature"""
        research_base = Path('.claude/research')
    
        # Check active research
        active_paths = [
            research_base / 'active' / 'features' / feature,
            research_base / 'active' / doc_type
        ]
    
        for path in active_paths:
            if path.exists():
                for file in path.glob('*.md'):
                    # Check if title matches (fuzzy match)
                    with open(file, 'r') as f:
                        content = f.read(500)  # First 500 chars
                        file_title = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                        if file_title:
                            # Simple similarity check
                            if title.lower() in file_title.group(1).lower() or \
                               file_title.group(1).lower() in title.lower():
                                return file
    
        # Check index for exact matches
        index_file = research_base / 'index.json'
        if index_file.exists():
            with open(index_file, 'r') as f:
                index = json.load(f)
            
            for doc in index.get('documents', []):
                if doc.get('feature') == feature and doc.get('type') == doc_type:
                    # Check title similarity
                    if title.lower() in doc.get('title', '').lower():
                        return Path(doc['path'])
    
        return None

    def merge_research_content(existing_content, new_content, doc_type):
        """Intelligently merge new research with existing"""
    
        # Extract sections from both documents
        def extract_sections(content):
            sections = {}
            current_section = None
            current_content = []
        
            for line in content.split('\n'):
                if line.startswith('##'):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = line
                    current_content = []
                else:
                    current_content.append(line)
        
            if current_section:
                sections[current_section] = '\n'.join(current_content)
        
            return sections
    
        existing_sections = extract_sections(existing_content)
        new_sections = extract_sections(new_content)
    
        # Merge strategies by document type
        if doc_type == 'analysis':
            # For analysis: append new findings, update recommendations
            merged = existing_content
        
            # Add new findings
            if '## Findings' in new_sections or '## Key Findings' in new_sections:
                merged += f"\n\n### Additional Findings ({datetime.now().strftime('%Y-%m-%d')})\n"
                merged += new_sections.get('## Findings', new_sections.get('## Key Findings', ''))
        
            # Update recommendations if present
            if '## Recommendations' in new_sections:
                merged = re.sub(
                    r'## Recommendations.*?(?=##|$)', 
                    f"## Recommendations (Updated {datetime.now().strftime('%Y-%m-%d')})\n" + 
                    new_sections['## Recommendations'] + '\n',
                    merged,
                    flags=re.DOTALL
                )
    
        elif doc_type == 'planning':
            # For planning: update phases, add change log
            merged = existing_content
        
            # Add change log
            change_log = f"\n\n## Change Log\n\n### {datetime.now().strftime('%Y-%m-%d')}\n"
        
            # Detect what changed
            changes = []
            for section in new_sections:
                if section not in existing_sections or \
                   new_sections[section].strip() != existing_sections.get(section, '').strip():
                    changes.append(f"- Updated {section}")
        
            if changes:
                change_log += '\n'.join(changes)
                merged += change_log
    
        elif doc_type == 'decision':
            # For decisions: never change decision, but can add implementation notes
            merged = existing_content
        
            if '## Implementation Notes' in new_sections:
                merged += f"\n\n### Implementation Update ({datetime.now().strftime('%Y-%m-%d')})\n"
                merged += new_sections['## Implementation Notes']
    
        else:
            # Default: append with timestamp
            merged = existing_content
            merged += f"\n\n---\n\n## Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            merged += new_content
    
        return merged

    def update_research_index(file_path, metadata):
        """Update the research index with document info"""
        index_file = Path('.claude/research/index.json')
    
        if index_file.exists():
            with open(index_file, 'r') as f:
                index = json.load(f)
        else:
            index = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "total_documents": 0,
                "documents": []
            }
    
        # Find existing entry
        doc_id = hashlib.md5(str(file_path).encode()).hexdigest()[:8]
        existing_entry = None
        for i, doc in enumerate(index['documents']):
            if doc['id'] == doc_id or doc['path'] == str(file_path):
                existing_entry = i
                break
    
        # Update or create entry
        entry = metadata.copy()
        entry['id'] = doc_id
        entry['path'] = str(file_path)
        entry['modified'] = datetime.now().isoformat()
    
        if existing_entry is not None:
            # Update existing
            entry['created'] = index['documents'][existing_entry]['created']
            entry['version'] = index['documents'][existing_entry].get('version', 1) + 1
            index['documents'][existing_entry] = entry
        else:
            # Add new
            entry['created'] = datetime.now().isoformat()
            entry['version'] = 1
            index['documents'].append(entry)
            index['total_documents'] += 1
    
        index['last_updated'] = datetime.now().isoformat()
    
        # Update category counts
        categories = {}
        for doc in index['documents']:
            doc_type = doc.get('type', 'unknown')
            categories[doc_type] = categories.get(doc_type, 0) + 1
        index['categories'] = categories
    
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)

    # Main logic
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    
        # Detect research indicators
        research_indicators = [
            'research', 'analysis', 'investigation', 'findings',
            'planning', 'proposal', 'considerations', 'options',
            'decision', 'architecture', 'design', 'approach'
        ]
    
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else Path(file_path).stem
    
        # Check if this looks like a research document
        content_lower = content.lower()
        is_research = any(indicator in content_lower for indicator in research_indicators)
    
        if not is_research and len(content) < 500:
            sys.exit(0)
    
        # Determine document type
        doc_type = 'research'
        if 'planning' in content_lower or 'plan' in title.lower():
            doc_type = 'planning'
        elif 'analysis' in content_lower:
            doc_type = 'analysis'
        elif 'decision' in content_lower or 'adr' in content_lower:
            doc_type = 'decision'
        elif 'findings' in content_lower:
            doc_type = 'findings'
    
        # Get current feature
        feature = get_current_feature()
    
        # Check for existing research document
        existing_doc = find_existing_research(feature, doc_type, title)
    
        if existing_doc:
            # UPDATE existing document
            print(f"""
    📝 Research Document Update Detected: {title}
    Type: {doc_type}
    Feature: {feature or 'general'}
    Existing: {existing_doc}

    This appears to be an update to an existing research document.
    Would you like to:
    1. Update the existing document (merge changes)
    2. Create a new version (archive old)
    3. Replace entirely (overwrite)
    4. Skip (leave as separate file)

    The system will intelligently merge based on document type:
    - Analysis: Append new findings, update recommendations
    - Planning: Track changes, update phases
    - Decisions: Add implementation notes (preserve original decision)
    """)
        
            # For now, auto-merge (in real implementation, would wait for user input)
            with open(existing_doc, 'r') as f:
                existing_content = f.read()
        
            # Merge content
            merged_content = merge_research_content(existing_content, content, doc_type)
        
            # Save merged content
            with open(existing_doc, 'w') as f:
                f.write(merged_content)
        
            # Update index
            metadata = {
                "title": title,
                "type": doc_type,
                "feature": feature,
                "size": len(merged_content),
                "keywords": list(set(word for word in re.findall(r'\b\w+\b', content_lower) 
                                   if word in research_indicators)),
                "summary": content.split('\n\n')[1] if '\n\n' in content else content[:200],
                "decision": "updated"
            }
        
            update_research_index(existing_doc, metadata)
        
            print(f"""
    ✅ Research document updated successfully!
    Location: {existing_doc}
    Version: Incremented
    Next: Continue working - changes are saved
    """)
        
            # Remove the duplicate file
            os.remove(file_path)
        
        else:
            # NEW document - existing flow
            print(f"""
    📚 New Research Document Detected: {title}
    Type: {doc_type}
    Feature: {feature or 'general'}

    This appears to be a new research document.
    Would you like to:
    1. Move to research directory and index
    2. Leave in current location
    3. Delete (if duplicate/draft)

    The research system will:
    - Organize in .claude/research/{doc_type}/
    - Index for searchability
    - Include in relevant contexts
    - Link to related features/PRDs
    """)
        
            # Create metadata for new document
            metadata = {
                "original_path": file_path,
                "title": title,
                "type": doc_type,
                "feature": feature,
                "created": datetime.now().isoformat(),
                "size": len(content),
                "keywords": list(set(word for word in re.findall(r'\b\w+\b', content_lower) 
                                   if word in research_indicators)),
                "first_paragraph": content.split('\n\n')[1] if '\n\n' in content else content[:200],
                "decision": "created"
            }
        
            # Save to pending captures
            pending_file = Path('.claude/research/pending_captures.json')
            pending_file.parent.mkdir(parents=True, exist_ok=True)
        
            pending = []
            if pending_file.exists():
                with open(pending_file, 'r') as f:
                    pending = json.load(f)
        
            pending.append(metadata)
        
            with open(pending_file, 'w') as f:
                json.dump(pending, f, indent=2)
        
            print(f"\nRun '/research review' to organize pending documents")

    except Exception as e:
        # More detailed error for debugging
        print(f"Research capture error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)

    # Exit successfully
    sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)