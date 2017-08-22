// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.

var PythonShell = require('python-shell');

LOGO_FILE = ""
PPTX_FILE = ""

basename = function (path) {
    return path.replace(/\\/g, '/').replace(/.*\//, '');
}

String.prototype.toUpperCaseFirstChar = function () {
    return this.substr(0, 1).toUpperCase() + this.substr(1);
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
        scriptPath: 'slidedeck_transform',
        args: ['--file', filename]
    };

    PythonShell.run('cli_list_metadata.py', options, function (err, results) {
        if (err) throw err;

        createInputList(JSON.parse(results).tags, JSON.parse(results).templates)
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

    templates = $("#templates_container input")
    try {
        Array.prototype.forEach.call(templates, function (template) {
            if (template.value == "") {
                alert("Input a value for the template '" + template.getAttribute("data-templatename") + "'")
                templates_bool = true
                throw BreakException;
            }
        });
    }
    catch (e) {
        return
    }

    dialogOptions = {
        title: "Save Powerpoint Presentation",
        defaultPath: defaultOutputFilename(PPTX_FILE, "new"),
        filters: [
            { name: 'Powerpoint Presentation', extension: ['ppt', 'pptx'] }
        ]
    }

    dialog.showSaveDialog(dialogOptions, function (outFile) {
        if (outFile === undefined) return;

        var options = {
            mode: 'text',
            scriptPath: 'slidedeck_transform',
            pythonOptions: '-u',
            args: [
                '--file', PPTX_FILE,
                '--tags', tag_list,
                '--logo', LOGO_FILE,
                '--templates', getTemplateData(),
                '--out', outFile
            ]
        };

        $("#loading").fadeIn()

        $("#loading_text").fadeOut(function () {
            $(this).text("Generating Slidedeck...").fadeIn();
        });

        var pyshell = new PythonShell('cli_transform.py', options);

        pyshell.on('message', function (message) {
            // received a message sent from the Python script (a simple "print" statement)
            $("#loading_text").text("Generating Slidedeck...\n" + message)
            console.log(message);
        });

        pyshell.end(function (err, results) {
            if (err) {
                alert(err);
            } else {
                $("#loading_text").text("Done!")
            }
            $("#loading").delay(400).fadeOut()

        });

    });



}

getTagsToDelete = () => {
    unchecked = $("input:checkbox[name=tag-list]:not(:checked)")
    return unchecked.map(function (x) {
        return unchecked[x].getAttribute("data-tagname");
    });
}

getTemplateData = () => {
    templates = $("#templates_container input")
    data = templates.map(function (x) {
        a = { "name": null, "value": null }
        a["name"] = templates[x].getAttribute("data-templatename")
        a["value"] = templates[x].value
        return JSON.stringify(a)
    });

    return "[" + Array.prototype.join.call(data, ',') + "]";
}

createInputList = (tags, templates) => {
    container = document.getElementById('tag-list')
    container.innerHTML = ""
    console.log(tags)

    var templatesContainer = document.createElement('div');
    templatesContainer.id = "templates_container"
    var templatesHeader = document.createElement('div');
    templatesHeader.innerHTML = "<h2>Text Replacement</h2>"

    templatesContainer.appendChild(templatesHeader)

    templates.forEach(function (template_object) {
        var template = template_object.name
        var templateDiv = document.createElement('div');
        var templateLabel = document.createElement('label')
        var templateInput = document.createElement('input');
        templateDiv.id = "template_textbox_" + template
        templateInput.setAttribute('data-templatename', template)
        templateInput.id = template + "-input";
        templateLabel.innerHTML = template.toUpperCaseFirstChar() + ":"
        templateInput.placeholder = "Value for {{" + template + "}}";
        templateInput.value = template_object.default
        templateDiv.appendChild(templateLabel);
        templateDiv.appendChild(templateInput);
        templatesContainer.appendChild(templateDiv);
    });

    container.appendChild(templatesContainer)

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