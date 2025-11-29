#!/usr/bin/env python3
import re

# Read the HTML file
with open('/workspace/templates/index.html', 'r') as f:
    content = f.read()

# Replace the matrix input grid with table format
def replace_matrix_form(content):
    # Find the generateMatrixForm function
    pattern = r"(\s*let html = '<div class=\"form-section\"><h2><i class=\"fas fa-table\"></i> Matrix Cell Ranges</h2>';)(\s*html \+= '<div class=\"matrix-input-grid\">';)(.*?)(\s*html \+= '</div></div>';)"
    
    # Replacement for the table format
    replacement = r"""\1
                html += '<div class="matrix-input-table-container">';
                html += '<table class="matrix-input-table">';
                
                // Add header row with column indices
                html += '<thead><tr><th></th>';
                for (let j = 0; j < size; j++) {
                    html += `<th>Col ${j}</th>`;
                }
                html += '</tr></thead>';
                
                html += '<tbody>';
                for (let i = 0; i < size; i++) {
                    html += `<tr>`;
                    html += `<th>Row ${i}</th>`;
                    for (let j = 0; j < size; j++) {
                        html += `<td class="matrix-cell-input">
                            <div class="form-group">
                                <label>Min</label>
                                <input type="number" class="min-${i}-${j}" step="0.01" value="0">
                            </div>
                            <div class="form-group">
                                <label>Max</label>
                                <input type="number" class="max-${i}-${j}" step="0.01" value="1">
                            </div>
                            <div class="form-group">
                                <label>Step</label>
                                <input type="number" class="step-${i}-${j}" step="0.01" value="0.1" min="0.001">
                            </div>
                        </td>`;
                    }
                    html += '</tr>';
                }
                html += '</tbody></table></div></div>';"""
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    return new_content

# Apply the replacement
content = replace_matrix_form(content)

# Write the updated content back
with open('/workspace/templates/index.html', 'w') as f:
    f.write(content)

print("Matrix form updated to table format!")