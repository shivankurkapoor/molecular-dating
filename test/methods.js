var sangerElementNumber = 1;
var sangerFileUploadDict = {};
var ngsElementNumber = 1;
var ngsFileUploadDict = {};


function openForm(evt, formType) {
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
    document.getElementById(formType).style.display = "block";
    evt.currentTarget.className += " active";
}

function showDefault() {
    /*Setting Sanger Sequence Data form on display by default*/
    button = document.getElementById("ss-tab-button");
    tabcontent = document.getElementById("ss");
    tabcontent.style.display = "block";
    button.className += " active";
    loader = document.getElementById("loader-display");
    loader.style.display = "none";
}

function isAnyError(form) {
    return false;
}


function fillRequests(requests, dataType) {
    var key;
    var request;
    if (dataType == 'ss') {
        for (key in sangerFileUploadDict) {
            if (sangerFileUploadDict.hasOwnProperty(key)) {
                request = Object();
                request.file = 'fasta_file_' + key;
                request.align = document.getElementById('align-' + key).checked;
                request.hxb2 = document.getElementById('hxb2-' + key).checked;
                request.meta_data = sangerFileUploadDict[key];
                requests.push(request);
            }
        }
    }
    else if (dataType == 'ngs') {
        for (key in ngsFileUploadDict) {
            if (ngsFileUploadDict.hasOwnProperty(key)) {
                request = Object();
                request.forward_file = 'forward_file_' + key;
                request.backward_file = 'backward_file_' + key;
                request.meta_data = Object();
                request.meta_data.forward_file = ngsFileUploadDict[key]['forward'];
                request.meta_data.backward_file = ngsFileUploadDict[key]['backward'];
                requests.push(request);
            }
        }
    }
}


function fetch(request_id) {
    $.ajax({
        url: '/fetch',
        data: {'request_id': request_id},
        dataType: 'json',
        type: 'GET',
        success: function (data) {
            //alert('SUCCESS');
            request_id = data['request_id'];
            user_id = data['user_id'];
            status = data['code'];
            //6002 is not processed
            window.location.assign("http://localhost:5000/displaypage?request_id=" + request_id + "&user_id=" + user_id + "&status=" + status);

        },
        complete: function () {
        },
        error: function (data) {
            alert('Error in second Ajax call');
        }
    });
}

function upload(form) {
    var requests = [];
    var formType;
    var dataType;
    var request;
    var formData;
    var numReq;
    if (form.id == 'ss-single-input-form') {
        if (!isAnyError(form)) {
            formType = 'single';
            dataType = 'ss';
            request = Object();
            request.file = 'fasta_file_0';
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
                async: false,
                success: function (data) {
                    //alert(data['request_id']);
                    document.getElementById("loader-msg").innerHTML = 'Request Id:' + data['request_id'] + '. Your request is being processed. ' +
                        'Please wait or keep note of your request id and check the status of your ' +
                        'request later.';
                    document.getElementById("ss").style.display = 'none';
                    document.getElementById("loader-display").style.display = 'block';
                    fetch(data['request_id'])
                },

                error: function () {
                    alert('Error in first Ajax call');
                }
            });

        }
    }

    else if (form.id == 'ngs-single-input-form') {
        if (!isAnyError(form)) {
            formType = 'single';
            dataType = 'ngs';
            request = Object();
            request.forward_file = 'forward_file_0';
            request.backward_file = 'backward_file_0';
            var forwardFile = form.elements['forwardfile'].files[0];
            var backwardFile = form.elements['backwardfile'].files[0];
            numReq = 1;
            requests.push(request);
            formData = new FormData();
            formData.append('form_type', formType);
            formData.append('data_type', dataType);
            formData.append('form_data', JSON.stringify({'requests': requests}));
            formData.append('num_request', numReq);
            formData.append('forward_file', forwardFile);
            formData.append('backward_file', backwardFile);

            $.ajax({
                url: '/upload',
                data: formData,
                processData: false,
                contentType: false,
                type: 'POST',
                async: false,
                success: function (data) {
                    document.getElementById("loader-msg").innerHTML = 'Request Id:' + data['request_id'] + '. Your request is being processed. ' +
                        'Please wait or keep note of your request id and check the status of your ' +
                        'request later.';
                    document.getElementById("ngs").style.display = 'none';
                    document.getElementById("loader-display").style.display = 'block';
                    fetch(data['request_id'])
                },
                error: function () {
                    alert('Error in first Ajax call');
                }
            });

        }

    }
    else if (form.id == 'ss-multi-input-form') {
        if (!isAnyError(form)) {
            formType = 'multiple';
            dataType = 'ss';
            fillRequests(requests, dataType);
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
                   // alert(data['status']);
                    if (data['status'] == 'ok') {
                        window.location.href = "/displaypage?request_id=" + data['request_id'] + "&user_id=" + data['user_id'] + "&status=0";
                    }
                    else {
                        window.location.href = '/error'
                    }
                },
                error: function () {

                }
            });
        }
    }
    else if (form.id == 'ngs-multi-input-form') {
        if (!isAnyError(form)) {
            formType = 'multiple';
            dataType = 'ngs';
            fillRequests(requests, dataType);
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
                   // alert(data['status']);
                    if (data['status'] == 'ok') {
                        window.location.href = "/displaypage?request_id=" + data['request_id'] + "&user_id=" + data['user_id'] + "&status=0";
                    }
                    else {
                        window.location.href = '/error'
                    }
                },
                error: function () {

                }
            });
        }

    }

    else if (form.id == 'request-status-input-form') {
        if (!isAnyError(form)) {
            var request_id = form.elements['request-id'].value;
            document.getElementById("loader-msg").innerHTML = 'Request Id:' + request_id + '. Fetching your request.';
            document.getElementById("request-status").style.display = 'none';
            document.getElementById("loader-display").style.display = 'block';
            fetch(request_id);
        }
    }
    return false
}

function removeElement(element) {
    var dataType = element.id.split('-')[0];
    var elementId = element.id.split('-').pop();
    if (dataType == 'ss') {
        delete sangerFileUploadDict[elementId];
    }
    else if (dataType == 'ngs') {
        delete ngsFileUploadDict[elementId];
    }

    element.parentNode.removeChild(element);
}

function addSangerInputElements() {
    var formContainer = document.getElementById('ss-form-container');
    var div = document.createElement('div');
    div.id = 'ss-input-form-element-' + sangerElementNumber;

    var buttonLabel = document.createElement('label');
    buttonLabel.innerHTML = "Choose Fasta File : ";

    var pickerButton = document.createElement("button");
    pickerButton.id = "picker-" + sangerElementNumber;
    pickerButton.type = "button";
    pickerButton.innerHTML = "Select from Google Drive";

    var fileLabel = document.createElement("label");
    fileLabel.id = "file-select-" + sangerElementNumber;

    var pickerScript = document.createElement("script");
    pickerScript.innerHTML = "function initPicker_" + sangerElementNumber + "() { \
      var picker = new FilePicker({ \
        apiKey: 'AIzaSyAK4MtRgKB-EPXvE94oCtuma8kXaynaAes',  \
        clientId: '160430799521-om2977l800uepldismnau961cof27lti', \
        buttonEl: document.getElementById(\'" + pickerButton.id + "\'), \
        onSelect: function(file) {  \
          document.getElementById(\'" + fileLabel.id + "\').style.color=\"black\";  \
          document.getElementById(\'" + fileLabel.id + "\').innerHTML=file.title;  \
          sangerFileUploadDict[" + sangerElementNumber + "] = file;  \
        } \
      }); \
    }";


    var loadScript = document.createElement("script");
    loadScript.src = "https\://apis.google.com/js/client.js?onload=initPicker_" + sangerElementNumber;

    var labelAlign = document.createElement('label');
    labelAlign.for = "align-" + sangerElementNumber;
    labelAlign.innerHTML = "Align : ";

    var alignInput = document.createElement('input');
    alignInput.type = "checkbox";
    alignInput.id = "align-" + sangerElementNumber;
    alignInput.name = "align-" + sangerElementNumber;
    alignInput.value = "True";

    var labelHXB2 = document.createElement('label');
    labelHXB2.for = "hxb2-" + sangerElementNumber;
    labelHXB2.innerHTML = "HXB2 : ";

    var hxb2Input = document.createElement('input');
    hxb2Input.type = "checkbox";
    hxb2Input.id = "hxb2-" + sangerElementNumber;
    hxb2Input.name = "hxb2-" + sangerElementNumber;
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
    sangerElementNumber += 1;
}

function addNextGenInputElements() {
    var formContainer = document.getElementById('ngs-form-container');
    var div = document.createElement('div');
    div.id = 'ngs-input-form-element-' + ngsElementNumber;

    /*Creating input elements for forward file*/
    var forwardButtonLabel = document.createElement('label');
    forwardButtonLabel.innerHTML = "Choose Forward File : ";

    var pickerForwardButton = document.createElement("button");
    pickerForwardButton.id = "picker-forward-" + ngsElementNumber;
    pickerForwardButton.type = "button";
    pickerForwardButton.innerHTML = "Select from Google Drive";

    var forwardFileLabel = document.createElement("label");
    forwardFileLabel.id = "forward-file-select-" + ngsElementNumber;

    var forwardPickerScript = document.createElement("script");
    forwardPickerScript.innerHTML = "function initForwardPicker_" + ngsElementNumber + "() { \
      var picker = new FilePicker({ \
        apiKey: 'AIzaSyAK4MtRgKB-EPXvE94oCtuma8kXaynaAes',  \
        clientId: '160430799521-om2977l800uepldismnau961cof27lti', \
        buttonEl: document.getElementById(\'" + pickerForwardButton.id + "\'), \
        onSelect: function(file) {  \
          document.getElementById(\'" + forwardFileLabel.id + "\').style.color=\"black\";  \
          document.getElementById(\'" + forwardFileLabel.id + "\').innerHTML=file.title;  \
          if(!ngsFileUploadDict.hasOwnProperty(" + ngsElementNumber + ")){\
               ngsFileUploadDict[" + ngsElementNumber + "] = {}; \
          }\
          ngsFileUploadDict[" + ngsElementNumber + "][\"forward\"] = file;\
        } \
      }); \
    }";


    var forwardLoadScript = document.createElement("script");
    forwardLoadScript.src = "https\://apis.google.com/js/client.js?onload=initForwardPicker_" + ngsElementNumber;

    /*Creating input elements for backward file*/
    var backwardButtonLabel = document.createElement('label');
    backwardButtonLabel.innerHTML = "Choose Backward File : ";

    var pickerBackwardButton = document.createElement("button");
    pickerBackwardButton.id = "picker-backward-" + ngsElementNumber;
    pickerBackwardButton.type = "button";
    pickerBackwardButton.innerHTML = "Select from Google Drive";

    var backwardFileLabel = document.createElement("label");
    backwardFileLabel.id = "backward-file-select_" + ngsElementNumber;

    var backwardPickerScript = document.createElement("script");
    backwardPickerScript.innerHTML = "function initBackwardPicker_" + ngsElementNumber + "() { \
      var picker = new FilePicker({ \
        apiKey: 'AIzaSyAK4MtRgKB-EPXvE94oCtuma8kXaynaAes',  \
        clientId: '160430799521-om2977l800uepldismnau961cof27lti', \
        buttonEl: document.getElementById(\'" + pickerBackwardButton.id + "\'), \
        onSelect: function(file) {  \
          document.getElementById(\'" + backwardFileLabel.id + "\').style.color=\"black\";  \
          document.getElementById(\'" + backwardFileLabel.id + "\').innerHTML=file.title;  \
          if(!ngsFileUploadDict.hasOwnProperty(" + ngsElementNumber + ")){\
               ngsFileUploadDict[" + ngsElementNumber + "] = {}; \
          }\
          ngsFileUploadDict[" + ngsElementNumber + "][\"backward\"] = file;\
        } \
      }); \
    }";


    var backwardLoadScript = document.createElement("script");
    backwardLoadScript.src = "https\://apis.google.com/js/client.js?onload=initBackwardPicker_" + ngsElementNumber;


    var removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.id = "rb";
    removeButton.name = "rb";
    removeButton.innerHTML = 'Remove';
    removeButton.onclick = function () {
        removeElement(this.parentNode);
    };

    div.appendChild(forwardButtonLabel);
    div.appendChild(pickerForwardButton);
    div.appendChild(forwardFileLabel);
    div.appendChild(forwardPickerScript);
    div.appendChild(forwardLoadScript);
    div.appendChild(backwardButtonLabel);
    div.appendChild(pickerBackwardButton);
    div.appendChild(backwardFileLabel);
    div.appendChild(backwardPickerScript);
    div.appendChild(backwardLoadScript);
    div.appendChild(removeButton);
    formContainer.appendChild(div);
    ngsElementNumber += 1;
}