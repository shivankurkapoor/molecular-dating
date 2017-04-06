var fileUploadDict = {};
var elementNumber = 1;

function openForm(evt, sequenceDataType) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(sequenceDataType).style.display = "block";
    evt.currentTarget.className += " active";
}

function showDefault() {
    //Setting Sanger Sequencing tab content on display by default
    button = document.getElementById("ssbutton");
    tabcontent = document.getElementById("ss");
    tabcontent.style.display = "block";
    button.class += " active";
}

function isAnyError(form) {
    return false;
}


function fillRequests(requests, dataType) {
    if (dataType == 'ss') {
        for (var key in fileUploadDict) {
            if (fileUploadDict.hasOwnProperty(key)) {
                var request = Object;
                var input_form_element = document.getElementById('input_form_id_' + key);
                request.algin = input_form_element

                    requests.push(JSON.stringify(fileUploadDict[key]));
            }
        }
    }
    else if(dataType == 'ngs'){

    }

}


function upload(form) {
    var requests = [];
    var formType;
    var dataType;
    var request;
    var formData;
    var numReq;
    if (form.id == 'ss_single_form') {
        if (!isAnyError(form)) {
            formType = 'single';
            dataType = 'ss';
            request = Object();
            request.file = 'fastafile_1';
            request.align = form.elements['align'].checked;
            request.hxb2 = form.elements['hxb2'].checked;
            var fastaFile = form.elements['fastafile'].files[0];
            numReq = 1;
            requests.push(request);
            formData = new FormData();
            formData.append('form_type', formType);
            formData.append('data_type', dataType);
            formData.append('form_data', JSON.stringify({'requests': requests}));
            formData.append('num_request', numReq);
            formData.append('fasta_file_0', fastaFile);

            $.ajax({
                url: '/upload',
                data: formData,
                processData: false,
                contentType: false,
                type: 'POST',
                success: function (data) {
                    alert("Response received");
                    window.location.href = "/";
                }
            });


        }
    }
    else if (form.id == 'ngs_single_form') {
        if (!isAnyError(form)) {
            formType = 'single';
            dataType = 'ngs';
            request = Object();
            request.forwardFile = 'forward_file_0';
            request.backwardFile = 'backward_file_0';
            var forwardFile = form.elements['forwardfile'].files[0];
            var backwardFile = form.elements['backwardfile'].files[0];
            numReq = 1;
            requests.push(request);
            formData = new FormData();
            formData.append('form_type', formType);
            formData.append('data_type', dataType);
            formData.append('form_data', JSON.stringify({'requests': requests}));
            formData.append('num_request', numReq);
            formData.append('forward_file_0', forwardFile);
            formData.append('backward_file_0', backwardFile);

            $.ajax({
                url: '/upload',
                data: formData,
                processData: false,
                contentType: false,
                type: 'POST',
                success: function (data) {
                    alert("Response received");
                    window.location.href = "/";
                }
            });

        }

    }
    else if (form.id == 'ss_multi_form') {
        if (!isAnyError(form)) {
            formType = 'multiple';
            dataType = 'ss';
            fillRequests(requests);
            numReq = requests.length;
            formData = new FormData();
            formData.append('form_type', formType);
            formData.append('data_type', dataType);
            formData.append('form_data', JSON.stringify({'requests': requests}));
            formData.append('num_request', numReq);
            $.ajax({
                url: '/upload',
                data: formData,
                processData: false,
                contentType: false,
                type: 'POST',
                success: function (data) {
                    alert("Response received");
                    window.location.href = "/";
                }
            });
        }
    }
    else if (form.id == 'ngs_multi_form') {
        if (!isAnyError(form)) {

        }

    }
    return false
}

function removeElement(element) {
    var elementId = element.id;
    delete fileUploadDict[elementId];
    element.parentNode.removeChild(element);
}

function addSangerFileChooser() {
    var formContainer = document.getElementById('ss_form_container');
    var div = document.createElement('div');
    div.id = 'input_form_element_' + elementNumber;

    var buttonLabel = document.createElement('label');
    buttonLabel.for = "fastafile";
    buttonLabel.innerHTML = "Choose Fasta File : ";

    var pickerButton = document.createElement("button");
    pickerButton.id = "picker_" + elementNumber;
    pickerButton.type = "button";
    pickerButton.innerHTML = "Select from Google Drive";

    var fileLabel = document.createElement("label");
    fileLabel.id = "file_select_" + elementNumber;

    var pickerScript = document.createElement("script");
    pickerScript.innerHTML = "function initPicker_" + elementNumber + "() { \
      var picker = new FilePicker({ \
        apiKey: 'AIzaSyAK4MtRgKB-EPXvE94oCtuma8kXaynaAes',  \
        clientId: '160430799521-om2977l800uepldismnau961cof27lti', \
        buttonEl: document.getElementById(\'" + pickerButton.id + "\'), \
        onSelect: function(file) {  \
          document.getElementById(\'" + fileLabel.id + "\').style.color=\"black\";  \
          document.getElementById(\'" + fileLabel.id + "\').innerHTML=file.title;  \
          fileUploadDict[" + elementNumber + "] = file;  \
        } \
      }); \
    }";


    var loadScript = document.createElement("script");
    loadScript.src = "https\://apis.google.com/js/client.js?onload=initPicker_" + elementNumber;

    var labelAlign = document.createElement('label');
    labelAlign.for = "align";
    labelAlign.innerHTML = "Align : ";

    var alignInput = document.createElement('input');
    alignInput.type = "checkbox";
    alignInput.id = "align";
    alignInput.name = "align";
    alignInput.value = "True";

    var labelHXB2 = document.createElement('label');
    labelHXB2.for = "hxb2";
    labelHXB2.innerHTML = "HXB2 : ";

    var hxb2Input = document.createElement('input');
    hxb2Input.type = "checkbox";
    hxb2Input.id = "hxb2";
    hxb2Input.name = "hxb2";
    hxb2Input.value = "True";

    var removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.id = "rb";
    removeButton.name = "rb";
    removeButton.innerHTML = 'Remove';
    removeButton.onclick = function () {
        removeElement(this.parentNode);
    };

    div.appendChild(buttonLabel);
    div.appendChild(pickerButton);
    div.appendChild(fileLabel);
    div.appendChild(pickerScript);
    div.appendChild(loadScript);
    div.appendChild(labelAlign);
    div.appendChild(alignInput);
    div.appendChild(labelHXB2);
    div.appendChild(hxb2Input);
    div.appendChild(removeButton);
    formContainer.appendChild(div);
    elementNumber += 1;
}