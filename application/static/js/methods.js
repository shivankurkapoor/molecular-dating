var fileUploadList = {};

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

function upload(form) {
    var requests = [];
    var formtype;
    var datatype;
    var request;
    var formdata;
    var numreq;
    if (form.id == 'ss_single_form') {
        if (!isAnyError(form)) {
            formtype = 'single';
            datatype = 'ss';
            request = Object();
            request.file = 'fastafile_1';
            request.align = form.elements['align'].checked;
            request.hxb2 = form.elements['hxb2'].checked;
            var fastafile = form.elements['fastafile'].files[0];
            numreq = 1;
            requests.push(request);
            formdata = new FormData();
            formdata.append('formtype', formtype);
            formdata.append('datatype', datatype);
            formdata.append('formdata', JSON.stringify({'requests':requests}));
            formdata.append('numreq', numreq);
            formdata.append('fastafile_1', fastafile);

            $.ajax({
                url: '/upload',
                data: formdata,
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
        if(!isAnyError(form)){
                formtype = 'single';
                datatype = 'ngs';
                request = Object();
                request.forward_file = 'forward_file_1';
                request.backward_file = 'backward_file_1';
                var forward_file = form.elements['forwardfile'].files[0];
                var backward_file = form.elements['backwardfile'].files[0];
                numreq = 1;
                requests.push(request);
                formdata = new FormData();
                formdata.append('formtype', formtype);
                formdata.append('datatype', datatype);
                formdata.append('formdata', JSON.stringify({'requests':requests}));
                formdata.append('numreq', numreq);
                formdata.append('forward_file_1', forward_file);
                formdata.append('backward_file_1', backward_file);

                 $.ajax({
                url: '/upload',
                data: formdata,
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
    else if (form.id == '') {

    }
    else if (form.id == '') {

    }
    return false
}

function removeElement(element) {
    element.parentNode.removeChild(element);
}

function addSangerFileChooser() {
    var form_container = document.getElementById('ss_form_container');
    var div = document.createElement('div');

    var labelfile = document.createElement('label');
    labelfile.for = "fastafile";
    labelfile.innerHTML = "Choose Fasta File : ";

    var fastabutton = document.createElement("button");
    fastabutton.id = "fastabutton";
    fastabutton.innerHTML = "Select from Google Drive";

    var fastaLabel = document.createElement("label");
    fastaLabel.id = "fastaLabel";

    var fastaScript = document.createElement("script");
    fastaScript.innerHTML = "function init" + fastabutton.id + "1Picker() { \
      var picker = new FilePicker({ \
        apiKey: 'AIzaSyAK4MtRgKB-EPXvE94oCtuma8kXaynaAes',  \
        clientId: '160430799521-om2977l800uepldismnau961cof27lti', \
        buttonEl: document.getElementById(\'" + fastabutton.id + "\'), \
        onSelect: function(file) {  \
          console.log(file);  \
          document.getElementById(\'" + fastaLabel.id + "\').style.color=\"black\";  \
          document.getElementById(\'" + fastaLabel.id + "\').innerHTML=file.title;  \
          var fileJson = {};  \
          fileJson['fileid'] = file['id'];  \
          fileJson['parentid'] = file['parents'][0]['id'];  \
          fileJson['filename'] = file['title']; \
          fileUploadList['Group" + elementNumber + "']['Sample" + i + "']['Forward'] = fileJson;  \
        } \
      }); \
    }";


    var loadScript = document.createElement("script");
    loadScript.src = "https\://apis.google.com/js/client.js?onload=init" + forward.id + "1Picker";

    var labelalign = document.createElement('label');
    labelalign.for = "align";
    labelalign.innerHTML = "Align : ";
    var aligninput = document.createElement('input');
    aligninput.type = "checkbox";
    aligninput.id = "align";
    aligninput.name = "align";
    aligninput.value = "True";

    var labelhxb2 = document.createElement('label');
    labelhxb2.for = "hxb2";
    labelhxb2.innerHTML = "HXB2 : ";
    var hxb2input = document.createElement('input');
    hxb2input.type = "checkbox";
    hxb2input.id = "hxb2";
    hxb2input.name = "hxb2";
    hxb2input.value = "True";

    var removebuttom = document.createElement('button');
    removebuttom.type = 'button';
    removebuttom.id = "rb";
    removebuttom.name = "rb";
    removebuttom.innerHTML = 'Remove';
    removebuttom.onclick = function() {removeElement(this.parentNode);};

    div.appendChild(labelfile);
    div.appendChild(fastabutton);
    div.appendChild(fastaLabel);
    div.appendChild(fastaScript);
    div.appendChild(loadScript);
    div.appendChild(labelalign);
    div.appendChild(aligninput);
    div.appendChild(labelhxb2);
    div.appendChild(hxb2input);
    div.appendChild(removebuttom);
    form_container.appendChild(div);
}