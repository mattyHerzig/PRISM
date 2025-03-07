import re

def analyze_diff(diff_content):
    """
    Analyzes the diff content and categorizes it into added, removed, and modified changes.

    Args:
        diff_content (str): The raw diff content as a string.

    Returns:
        dict: A dictionary with categories 'added', 'removed', and 'modified' containing lists of changes.
    """
    changes = {
        "added": [],
        "removed": [],
        "modified": []
    }

    # Split the diff content by lines for processing
    lines = diff_content.splitlines()
    file_changes = []
    current_file = {"file_name": None, "added": [], "removed": []}

    # Regular expression to capture file name in the diff
    file_header_pattern = re.compile(r"^diff --git a/(.+) b/(.+)")

    for line in lines:
        # Detect file headers and reset the current file changes
        match = file_header_pattern.match(line)
        if match:
            if current_file["file_name"]:
                file_changes.append(current_file)
            current_file = {
                "file_name": match.group(1),
                "added": [],
                "removed": []
            }
            continue

        # Capture added, removed, or modified lines within the file
        if line.startswith("+") and not line.startswith("+++"):
            # Line added (ignoring file header lines like +++)
            current_file["added"].append(line[1:].strip())
        elif line.startswith("-") and not line.startswith("---"):
            # Line removed (ignoring file header lines like ---)
            current_file["removed"].append(line[1:].strip())

    # Append any remaining changes for the last file in the diff
    if current_file["file_name"]:
        file_changes.append(current_file)

    # Analyze each file change for modifications
    for file_change in file_changes:
        added_lines = file_change["added"]
        removed_lines = file_change["removed"]

        # Simple heuristic to detect modifications by pairing added and removed lines
        if len(added_lines) > 0 and len(removed_lines) > 0:
            changes["modified"].append({
                "file": file_change["file_name"],
                "added": added_lines,
                "removed": removed_lines
            })
        else:
            if added_lines:
                changes["added"].append({
                    "file": file_change["file_name"],
                    "lines": added_lines
                })
            if removed_lines:
                changes["removed"].append({
                    "file": file_change["file_name"],
                    "lines": removed_lines
                })

    return changes
