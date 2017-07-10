// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.

var PythonShell = require('python-shell');

LOGO_FILE = ""
PPTX_FILE = ""

basename = function (path) {
    return path.replace(/\\/g, '/').replace(/.*\//, '');
}

// Make paths work on windows and unix
normalise = (filepath) => {
    return filepath.replace(/ /g, "%20").replace(/\\/g, '/')
}

var pptx_drag_drop = document.getElementById('drag-drop-pptx');

pptx_drag_drop.ondragover = () => {
    return false;
};

pptx_drag_drop.ondragleave = () => {
    return false;
};

pptx_drag_drop.ondragend = () => {
    return false;
};

pptx_drag_drop.ondrop = (e) => {
    e.preventDefault();
    filename = e.dataTransfer.files[0].path

    $(pptx_drag_drop).text(basename(filename))
    PPTX_FILE = filename

    var options = {
        mode: 'text',
        scriptPath: '..',
        args: ['--file', filename]
    };

    PythonShell.run('cli_list_metadata.py', options, function (err, results) {
        if (err) throw err;

        // alert("data:" + results);
        createTagList(JSON.parse(results).tags)
    });

    return false;
};

var logo_drag_drop = document.getElementById('drag-drop-logo');

logo_drag_drop.ondragover = () => {
    return false;
};

logo_drag_drop.ondragleave = () => {
    return false;
};

logo_drag_drop.ondragend = () => {
    return false;
};

logo_drag_drop.ondrop = (e) => {
    e.preventDefault();

    filename = e.dataTransfer.files[0].path
    $(logo_drag_drop).text("")
    // $(logo_drag_drop).css("background","url('" + filename + "')")  
    console.log(normalise(filename))
    $(logo_drag_drop).css("backgroundImage", "url('file://" + normalise(filename) + "')")
    LOGO_FILE = filename
    return false;
};

defaultOutputFilename = (filename, client) => {
    return filename.replace(".ppt", "-" + client + ".ppt")
}

var resetButton = document.getElementById('reset')
resetButton.onclick = () => {
    location.reload();
}

var submitButton = document.getElementById('submit')

submitButton.onclick = () => {


    tag_list = Array.prototype.join.call(getTagsToDelete(), ',');

    if (!PPTX_FILE) {
        alert("Select a powerpoint file")
        return
    }

    if (!LOGO_FILE) {
        alert("Select a logo file")
        return
    }

    if (!getClientName()) {
        alert("Input a client name")
        return
    }

    dialogOptions = {
        title: "Save Powerpoint Presentation",
        defaultPath: defaultOutputFilename(PPTX_FILE, getClientName()),
        filters: [
            { name: 'Powerpoint Presentation', extension: ['ppt', 'pptx'] }
        ]
    }

    dialog.showSaveDialog(dialogOptions, function (outFile) {
        if (outFile === undefined) return;

        var options = {
            mode: 'text',
            scriptPath: '..',
            args: [
                '--file', PPTX_FILE,
                '--tags', tag_list,
                '--logo', LOGO_FILE,
                '--client', getClientName(),
                '--out', outFile
            ]
        };

        PythonShell.run('cli_transform.py', options, function (err, results) {
            if (err) {
                alert(err);
            } else {
                alert("Done!");
            }

        });
    });



}

getTagsToDelete = () => {
    unchecked = $("input:checkbox[name=tag-list]:not(:checked)")
    return unchecked.map(function (x) {
        return unchecked[x].getAttribute("data-tagname");
    });
}

getClientName = () => {
    return $("#client-input").val()
}

createTransformCommand = (pptx, logo, tags) => {
    tag_list = Array.prototype.join.call(tags, ',');
    return 'python cli_transform.py --file "' + PPTX_FILE + ' --tags "' + tag_list + '" --logo "' + LOGO_FILE + '"' + '--client "' + getClientName() + '"';
}

createTagList = (tags) => {
    container = document.getElementById('tag-list')
    container.innerHTML = ""
    console.log(tags)

    var templatesHeader = document.createElement('div');
    templatesHeader.innerHTML = "<h2>Text Replacement</h2>"

    container.appendChild(templatesHeader)


    var clientDiv = document.createElement('div');
    var clientLabel = document.createElement('label')
    var clientInput = document.createElement('input');
    clientDiv.id = "client"
    clientInput.id = "client-input";
    clientLabel.innerHTML = "Client:"
    clientInput.placeholder = "The name of the client";
    clientDiv.appendChild(clientLabel);
    clientDiv.appendChild(clientInput);
    container.appendChild(clientDiv);

    var tagDiv = document.createElement('div');
    if (tags.length == 0) {
        tagDiv.innerHTML = "No tags found in presentation"
    } else {
        tagDiv.innerHTML = "<h2>Tags to keep</h2>"
    }

    container.appendChild(tagDiv)

    tags.forEach(function (tag) {

        var div = document.createElement('div');
        div.class = "checkbox"

        var checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.name = "tag-list";
        checkbox.checked = true;
        checkbox.id = "tag_checkbox_" + tag;
        checkbox.setAttribute('data-tagname', tag)

        var label = document.createElement('label')
        label.htmlFor = "tag_checkbox_" + tag;
        label.appendChild(document.createTextNode(tag));

        div.appendChild(checkbox);
        div.appendChild(label);
        container.appendChild(div)
    }, this);
}