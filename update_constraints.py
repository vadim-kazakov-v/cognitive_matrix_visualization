#!/usr/bin/env python3
import re

# Read the HTML file
with open('/workspace/templates/index.html', 'r') as f:
    content = f.read()

# Define the pattern to find the constraint matrix grid creation
pattern = r"(let matrixGridHtml = '<div class=\"matrix-cell-grid\" data-constraint-id=\"\$\{constraintCount\}\">';\s+for \(let i = 0; i < size; i\+\+\) \{\s+for \(let j = 0; j < size; j\+\+\) \{\s+matrixGridHtml \+= `<div class=\"matrix-cell-item\" data-cell=\"\$\{i\},\$\{j\}\">\\[\$\{i\}\\]\\[\$\{j\}\\]</div>`;\s+\}\s+\}\s+matrixGridHtml \+= '</div>';)"

# Replacement for table format
replacement = """let matrixGridHtml = '<table class="matrix-cell-grid" data-constraint-id="${constraintCount}"><tbody>';
                for (let i = 0; i < size; i++) {
                    matrixGridHtml += '<tr>';
                    for (let j = 0; j < size; j++) {
                        matrixGridHtml += `<td><div class="matrix-cell-item" data-cell="${i},${j}">[${i}][${j}]</div></td>`;
                    }
                    matrixGridHtml += '</tr>';
                }
                matrixGridHtml += '</tbody></table>';"""

# Perform the replacement
new_content = re.sub(pattern, replacement, content)

# Write the updated content back
with open('/workspace/templates/index.html', 'w') as f:
    f.write(new_content)

print("Constraint matrix grid updated to table format!")