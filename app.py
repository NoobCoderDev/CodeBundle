import streamlit as st

st.set_page_config(page_title="CodeBundle", layout="wide")

st.title("📁 CodeBundle")
st.write("Combine multiple code files into a single copyable format for LLMs")

drag_drop_html = """
<div id="drop-area" style="
    border: 2px dashed #ccc;
    border-radius: 10px;
    padding: 40px;
    text-align: center;
    margin: 20px 0;
    background-color: #f9f9f9;
    cursor: pointer;
    transition: all 0.3s ease;
">
    <p style="font-size: 18px; color: #666;">
        📄 Drag and drop individual code files here<br>
        <small>Files only - folders need the button below</small>
    </p>
</div>

<div style="margin: 15px 0; text-align: center; background: #fff3cd; padding: 15px; border-radius: 8px; border: 1px solid #ffeaa7;">
    <p style="margin: 0 0 10px 0; color: #856404;"><strong>⚠️ Browser Limitation:</strong> Drag-and-drop doesn't work for folders due to security restrictions.</p>
    <button id="folder-btn" style="
        background: #2196F3;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 5px;
        cursor: pointer;
        margin: 5px;
        font-size: 16px;
        font-weight: bold;
    ">📂 Select Folder (Recommended)</button>
    <button id="files-btn" style="
        background: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 5px;
        cursor: pointer;
        margin: 5px;
        font-size: 16px;
        font-weight: bold;
    ">📄 Select Multiple Files</button>
</div>

<!-- Exclude Folders Section -->
<div style="margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;">
    <h4 style="margin: 0 0 10px 0; color: #495057;">🚫 Exclude Folders</h4>
    <div style="margin: 10px 0;">
        <label style="display: block; margin: 5px 0; font-weight: bold;">
            <input type="checkbox" id="exclude-default" checked> Use Default Exclusions
        </label>
        <small style="color: #6c757d;">node_modules, __pycache__, .git, venv, env, build, dist, etc.</small>
    </div>
    
    <div style="margin: 15px 0;">
        <label style="display: block; margin: 5px 0; font-weight: bold;">Custom Exclude Folders:</label>
        <input type="text" id="custom-excludes" placeholder="e.g., temp, logs, cache (comma separated)" style="
            width: 100%;
            padding: 8px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 14px;
        ">
        <small style="color: #6c757d;">Add custom folder names to exclude (comma separated)</small>
    </div>
    
    <div style="margin: 10px 0;">
        <button id="show-excludes" style="
            background: #6c757d;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        ">👁️ Show Current Exclusions</button>
    </div>
</div>

<input type="file" id="file-input-folder" webkitdirectory multiple style="display: none;">
<input type="file" id="file-input-files" multiple accept=".py,.js,.html,.css,.java,.cpp,.c,.php,.rb,.go,.rs,.ts,.jsx,.tsx,.vue,.sql,.json,.xml,.yaml,.yml,.txt,.md,.htm,.sh,.bat,.ps1,.dockerfile,.gitignore,.env" style="display: none;">

<!-- File List with Scrollbar -->
<div id="file-list" style="margin: 20px 0;"></div>

<!-- Code Section with Fixed Height -->
<div id="code-section" style="
    margin: 20px 0; 
    display: none;
    min-height: 600px;
    border: 2px solid #4CAF50;
    border-radius: 10px;
    padding: 20px;
    background: #f8fff8;
">
    <h3 style="color: #333; margin: 0 0 15px 0;">📋 Combined Code</h3>
    
    <!-- Stats and Controls -->
    <div style="
        margin: 0 0 20px 0; 
        padding: 15px; 
        background: #e8f5e8; 
        border-radius: 8px; 
        border: 1px solid #4CAF50;
    ">
        <div id="code-stats" style="margin-bottom: 15px; font-size: 16px;"></div>
        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
            <button onclick="copyAllCode()" style="
                background: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                flex: 1;
                min-width: 150px;
            ">📋 Copy All Code</button>
            <button onclick="downloadCode()" style="
                background: #2196F3;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                flex: 1;
                min-width: 150px;
            ">📥 Download</button>
            <button onclick="togglePreview()" id="toggle-btn" style="
                background: #9c27b0;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
                flex: 1;
                min-width: 120px;
            ">👁️ Show Preview</button>
            <button onclick="clearAll()" style="
                background: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
                flex: 1;
                min-width: 100px;
            ">🗑️ Clear All</button>
        </div>
    </div>
    
    <!-- Code Preview Area -->
    <div style="
        border: 2px solid #ddd;
        border-radius: 8px;
        background: white;
        min-height: 400px;
    ">
        <textarea id="code-preview" style="
            width: calc(100% - 20px);
            height: 450px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            border: none;
            border-radius: 6px;
            padding: 15px;
            margin: 10px;
            display: none;
            resize: both;
            overflow-y: auto;
            overflow-x: auto;
            background: #fafafa;
            line-height: 1.4;
            min-height: 200px;
            max-height: 800px;
            min-width: 300px;
        " readonly placeholder="Code will appear here..."></textarea>
        
        <div id="large-code-message" style="
            display: none;
            padding: 40px;
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 6px;
            text-align: center;
            margin: 10px;
        ">
            <h4 style="margin: 0 0 10px 0;">📄 Large Codebase Detected</h4>
            <p style="margin: 0; color: #856404;">Code is ready but preview is hidden for performance. Use the buttons above to copy or download.</p>
        </div>
        
        <div id="no-preview-message" style="
            display: block;
            padding: 40px;
            text-align: center;
            color: #666;
            font-style: italic;
        ">
            <h4 style="margin: 0 0 10px 0;">📝 Code Preview</h4>
            <p style="margin: 0;">Preview will appear here after processing files</p>
        </div>
    </div>
</div>

<script>
let allFiles = [];
let combinedText = '';
let previewVisible = false;
const MAX_PREVIEW_SIZE = 500000; // 500KB limit for preview

const supportedExtensions = [
    'py', 'js', 'html', 'css', 'java', 'cpp', 'c', 'php', 'rb', 
    'go', 'rs', 'ts', 'jsx', 'tsx', 'vue', 'sql', 'json', 'xml', 
    'yaml', 'yml', 'txt', 'md', 'htm', 'sh', 'bat', 'ps1'
];

const defaultExcludedFolders = [
    'node_modules', '__pycache__', '.git', '.vscode', '.idea', 'dist', 'build', 'target',
    'bin', 'obj', '.next', '.nuxt', 'coverage', '.nyc_output', 'logs', '.DS_Store',
    'Thumbs.db', 'venv', 'env', '.env', '.venv', 'virtualenv', 'ENV', 'env.bak',
    'venv.bak', '.pytest_cache', '.mypy_cache', '.tox', 'out', 'output', 'public',
    'static', 'temp', 'tmp', 'cache', '.cache', 'vendor', 'bower_components', 'package-lock.json',
    'readme.md',
    '.env'
];

// Event listeners
document.getElementById('folder-btn').addEventListener('click', () => {
    document.getElementById('file-input-folder').click();
});

document.getElementById('files-btn').addEventListener('click', () => {
    document.getElementById('file-input-files').click();
});

document.getElementById('show-excludes').addEventListener('click', () => {
    const exclusions = getCurrentExclusions();
    alert('🚫 Current Exclusions:\\n\\n' + exclusions.join('\\n'));
});

document.getElementById('drop-area').addEventListener('click', () => {
    document.getElementById('file-input-files').click();
});

document.getElementById('drop-area').addEventListener('dragover', (e) => {
    e.preventDefault();
    e.currentTarget.style.backgroundColor = '#e8f5e8';
    e.currentTarget.style.borderColor = '#4CAF50';
});

document.getElementById('drop-area').addEventListener('dragleave', (e) => {
    e.currentTarget.style.backgroundColor = '#f9f9f9';
    e.currentTarget.style.borderColor = '#ccc';
});

document.getElementById('drop-area').addEventListener('drop', (e) => {
    e.preventDefault();
    e.currentTarget.style.backgroundColor = '#f9f9f9';
    e.currentTarget.style.borderColor = '#ccc';
    
    const files = Array.from(e.dataTransfer.files);
    const hasFolders = files.some(file => file.type === '' && !file.name.includes('.'));
    
    if (hasFolders) {
        alert('🚫 Folder drag-and-drop not supported! Use "📂 Select Folder" button.');
        return;
    }
    
    if (files.length === 0) {
        alert('⚠️ No files detected.');
        return;
    }
    
    handleFiles(files, false);
});

document.getElementById('file-input-folder').addEventListener('change', (e) => {
    handleFiles(e.target.files, true);
});

document.getElementById('file-input-files').addEventListener('change', (e) => {
    handleFiles(e.target.files, false);
});

function getCurrentExclusions() {
    let exclusions = [];
    if (document.getElementById('exclude-default').checked) {
        exclusions = [...defaultExcludedFolders];
    }
    const customExcludes = document.getElementById('custom-excludes').value.trim();
    if (customExcludes) {
        const customList = customExcludes.split(',').map(item => item.trim()).filter(item => item);
        exclusions = [...exclusions, ...customList];
    }
    return [...new Set(exclusions)];
}

function isExcludedPath(filePath) {
    const exclusions = getCurrentExclusions();
    const pathParts = filePath.toLowerCase().split('/');
    
    for (const part of pathParts) {
        if (exclusions.some(excluded => excluded.toLowerCase() === part)) {
            return true;
        }
    }
    
    const lowerPath = filePath.toLowerCase();
    for (const excluded of exclusions) {
        if (lowerPath.includes(excluded.toLowerCase() + '/') || 
            lowerPath.includes('/' + excluded.toLowerCase() + '/')) {
            return true;
        }
    }
    return false;
}

function isCodeFile(filename) {
    if (filename === 'Dockerfile' || filename === '.gitignore' || filename.startsWith('.env')) {
        return true;
    }
    const parts = filename.split('.');
    if (parts.length < 2) return false;
    const ext = parts[parts.length - 1].toLowerCase();
    return supportedExtensions.includes(ext);
}

function getRelativePath(file, isFolder) {
    if (isFolder && file.webkitRelativePath) {
        return file.webkitRelativePath;
    }
    return file.name;
}

function handleFiles(files, isFolder) {
    let filesProcessed = 0;
    const allFilesArray = Array.from(files);
    
    const filteredFiles = allFilesArray.filter(file => {
        const filePath = getRelativePath(file, isFolder);
        return !isExcludedPath(filePath);
    });
    
    const codeFiles = filteredFiles.filter(file => isCodeFile(file.name));
    const excludedCount = allFilesArray.length - filteredFiles.length;
    
    if (codeFiles.length === 0) {
        alert(`❌ No supported code files found!\\n\\nTotal: ${allFilesArray.length}, Excluded: ${excludedCount}, Code files: 0`);
        return;
    }
    
    updateStatus(`📋 Processing ${codeFiles.length} files (excluded ${excludedCount})...`);
    
    codeFiles.forEach((file) => {
        const filePath = getRelativePath(file, isFolder);
        
        const existingFile = allFiles.find(f => f.path === filePath);
        if (existingFile) {
            filesProcessed++;
            if (filesProcessed === codeFiles.length) {
                updateDisplay();
            }
            return;
        }
        
        const reader = new FileReader();
        
        reader.onload = function(e) {
            try {
                const content = e.target.result;
                const fileData = {
                    name: file.name,
                    path: filePath,
                    size: file.size,
                    content: content
                };
                
                allFiles.push(fileData);
                combinedText += `# ${filePath}\\n\\n${content}\\n\\n${'-'.repeat(50)}\\n\\n`;
                filesProcessed++;
                
                if (filesProcessed === codeFiles.length) {
                    updateDisplay();
                }
            } catch (error) {
                console.error('Error processing file:', filePath, error);
                filesProcessed++;
                if (filesProcessed === codeFiles.length) {
                    updateDisplay();
                }
            }
        };
        
        reader.onerror = function(error) {
            console.error('Error reading file:', filePath, error);
            filesProcessed++;
            if (filesProcessed === codeFiles.length) {
                updateDisplay();
            }
        };
        
        reader.readAsText(file);
    });
}

function updateDisplay() {
    // Show the code section
    document.getElementById('code-section').style.display = 'block';
    document.getElementById('no-preview-message').style.display = 'none';
    
    // Update stats
    const isLarge = combinedText.length > MAX_PREVIEW_SIZE;
    const sizeInMB = (combinedText.length / 1024 / 1024).toFixed(2);
    
    document.getElementById('code-stats').innerHTML = `
        <strong>📊 Stats:</strong> 
        ${allFiles.length} files | 
        ${combinedText.length.toLocaleString()} characters | 
        ${sizeInMB} MB
        ${isLarge ? ' | <span style="color: #ff6b35; font-weight: bold;">⚠️ Large codebase detected</span>' : ''}
    `;
    
    // Handle preview display
    const preview = document.getElementById('code-preview');
    const largeMessage = document.getElementById('large-code-message');
    const toggleBtn = document.getElementById('toggle-btn');
    
    if (isLarge) {
        preview.style.display = 'none';
        largeMessage.style.display = 'block';
        toggleBtn.textContent = '👁️ Force Show Preview';
        previewVisible = false;
    } else {
        largeMessage.style.display = 'none';
        preview.value = combinedText;
        preview.style.display = 'block';
        toggleBtn.textContent = '🙈 Hide Preview';
        previewVisible = true;
    }
    
    // Update file list with scrollbar
    const filesByDir = {};
    allFiles.forEach(file => {
        const dir = file.path.includes('/') ? file.path.substring(0, file.path.lastIndexOf('/')) : 'root';
        if (!filesByDir[dir]) filesByDir[dir] = [];
        filesByDir[dir].push(file.name);
    });
    
    let fileStructure = `
        <div style="
            background: #f0f0f0; 
            padding: 15px; 
            border-radius: 5px; 
            margin: 10px 0;
            max-height: 250px;
            overflow-y: auto;
            overflow-x: auto;
            border: 1px solid #ddd;
        ">
            <strong>📁 File Structure:</strong>
            <div style="margin-top: 10px;">
    `;
    
    Object.keys(filesByDir).sort().forEach(dir => {
        fileStructure += `<div style="margin: 8px 0; font-weight: bold; color: #2c3e50;">📂 ${dir}/</div>`;
        filesByDir[dir].forEach(fileName => {
            fileStructure += `<div style="margin-left: 25px; margin: 3px 0 3px 25px; color: #666; font-size: 14px;">📄 ${fileName}</div>`;
        });
    });
    
    fileStructure += '</div></div>';
    
    updateStatus(`<h3>✅ Successfully loaded ${allFiles.length} code files</h3>${fileStructure}`);
}

function updateStatus(html) {
    document.getElementById('file-list').innerHTML = html;
}

function copyAllCode() {
    const tempTextarea = document.createElement('textarea');
    tempTextarea.value = combinedText;
    document.body.appendChild(tempTextarea);
    tempTextarea.select();
    
    try {
        document.execCommand('copy');
        alert('✅ All code copied to clipboard!');
    } catch (err) {
        navigator.clipboard.writeText(combinedText).then(() => {
            alert('✅ All code copied to clipboard!');
        }).catch(() => {
            alert('❌ Copy failed. Try the download option.');
        });
    }
    
    document.body.removeChild(tempTextarea);
}

function downloadCode() {
    const blob = new Blob([combinedText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'combined_code.txt';
    a.click();
    URL.revokeObjectURL(url);
}

function togglePreview() {
    const preview = document.getElementById('code-preview');
    const largeMessage = document.getElementById('large-code-message');
    const toggleBtn = document.getElementById('toggle-btn');
    const isLarge = combinedText.length > MAX_PREVIEW_SIZE;
    
    if (previewVisible) {
        preview.style.display = 'none';
        if (isLarge) largeMessage.style.display = 'block';
        toggleBtn.textContent = isLarge ? '👁️ Force Show Preview' : '👁️ Show Preview';
        previewVisible = false;
    } else {
        if (isLarge && !confirm('⚠️ Large codebase may slow your browser. Continue?')) {
            return;
        }
        largeMessage.style.display = 'none';
        preview.value = combinedText;
        preview.style.display = 'block';
        toggleBtn.textContent = '🙈 Hide Preview';
        previewVisible = true;
    }
}

function clearAll() {
    allFiles = [];
    combinedText = '';
    document.getElementById('file-list').innerHTML = '';
    document.getElementById('code-section').style.display = 'none';
    document.getElementById('code-preview').value = '';
    document.getElementById('no-preview-message').style.display = 'block';
    document.getElementById('file-input-folder').value = '';
    document.getElementById('file-input-files').value = '';
    previewVisible = false;
}
</script>
"""

st.components.v1.html(drag_drop_html, height=1600)  # Increased height significantly

st.markdown("---")
st.markdown("**📋 How to Use:**")
st.markdown("1. **Select Files/Folder** using the buttons above")
st.markdown("2. **View File Structure** - scrollable list with all processed files")
st.markdown("3. **Copy Code** - click 'Copy All Code' to copy everything")
st.markdown("4. **Preview** - toggle preview on/off (hidden for large files)")
st.markdown("5. **Download** - save as .txt file for backup")

st.markdown("**Supported:** .py, .js, .html, .css, .java, .cpp, .c, .php, .rb, .go, .rs, .ts, .jsx, .tsx, .vue, .sql, .json, .xml, .yaml, .yml, .txt, .md, .sh, .bat, .ps1, Dockerfile, .env, .gitignore")
