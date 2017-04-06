var numberOfElementsInEachElementInContainer = 4;
var fileUploadList = {};

function addGroups() {
  fileUploadList = {};
  var number = document.getElementById("member").value;
  var container = document.getElementById("container");
  var count = container.childElementCount;
  while(container.hasChildNodes()) {
    container.removeChild(container.lastChild);
  }
  for(i = 0; i < number; i++) {
    fileUploadList['Group' + i] = {};
    container.appendChild(document.createTextNode("Group " + (i+1) + " Number of samples: "));

    var input = document.createElement("input");
    input.type = "text";
    input.id = "I" + i;
    container.appendChild(input);

    var buttonElement = document.createElement("button");
    buttonElement.id = "B" + i;
    buttonElement.innerHTML = "Add Samples";
    buttonElement.onclick = function() {addSamples(this);};
    container.appendChild(buttonElement);

    var divElement = document.createElement("div");
    divElement.id = "D" + i;
    container.appendChild(divElement);

    container.appendChild(document.createElement("br"));
  }
}

/*
function addSamples(element) {
  var id = element.id;
  var elementNumber = id.substring(1);
  var divElement = document.getElementById("D" + elementNumber);
  var number = document.getElementById("I" + elementNumber).value;
  while(divElement.hasChildNodes()) {
    divElement.removeChild(divElement.lastChild);
  }
  for(i = 0; i < number; i++) {
    divElement.appendChild(document.createTextNode("Sample " + (i+1) + ":"));
    divElement.appendChild(document.createElement("br"));

    divElement.appendChild(document.createTextNode("Forward File:\t"));
    var forward = document.createElement("input");
    forward.type = "text";
    forward.id = "G" + elementNumber + "F" + i;
    divElement.appendChild(forward);
    divElement.appendChild(document.createElement("br"));

    divElement.appendChild(document.createTextNode("Backward File:\t"));
    var backward = document.createElement("input");
    backward.type = "text";
    backward.id = "G" + elementNumber + "B" + i;
    divElement.appendChild(backward);

    divElement.appendChild(document.createElement("br"));
    divElement.appendChild(document.createElement("br"));
  }
}
*/

function addSamples(element) {
  var id = element.id;
  var elementNumber = id.substring(1);
  fileUploadList['Group' + elementNumber] = {};
  var divElement = document.getElementById("D" + elementNumber);
  var number = document.getElementById("I" + elementNumber).value;
  while(divElement.hasChildNodes()) {
    divElement.removeChild(divElement.lastChild);
  }
  for(i = 0; i < number; i++) {
    fileUploadList['Group' + elementNumber]['Sample' + i] = {};
    fileUploadList['Group' + elementNumber]['Sample' + i]['Forward'] = null;
    fileUploadList['Group' + elementNumber]['Sample' + i]['Backward'] = null;
    divElement.appendChild(document.createTextNode("Sample " + (i+1) + ":"));
    divElement.appendChild(document.createElement("br"));

    divElement.appendChild(document.createTextNode("Forward File:\t"));
    var forward = document.createElement("button");
    forward.id = "G" + elementNumber + "FB" + i;
    forward.innerHTML = "Select from Google Drive";
    divElement.appendChild(forward);

    var forwardLabel = document.createElement("label");
    forwardLabel.id = "G" + elementNumber + "FL" + i;
    divElement.appendChild(forwardLabel);

    var forwardScript = document.createElement("script")
    forwardScript.innerHTML = "function init" + forward.id + "1Picker() { \
      var picker = new FilePicker({ \
        apiKey: 'AIzaSyBrPcJgwBk7wZtCMpJ1Wz_AR_GlLQP1RGw',  \
        clientId: '23388632533-77bq0mev3uiumabgcl4r14ji10tk9687', \
        buttonEl: document.getElementById(\'" + forward.id + "\'), \
        onSelect: function(file) {  \
          console.log(file);  \
          document.getElementById(\'" + forwardLabel.id + "\').style.color=\"black\";  \
          document.getElementById(\'" + forwardLabel.id + "\').innerHTML=file.title;  \
          var fileJson = {};  \
          fileJson['fileid'] = file['id'];  \
          fileJson['parentid'] = file['parents'][0]['id'];  \
          fileJson['filename'] = file['title']; \
          fileUploadList['Group" + elementNumber + "']['Sample" + i + "']['Forward'] = fileJson;  \
        } \
      }); \
    }"
    divElement.appendChild(forwardScript);

    var loadScript = document.createElement("script");
    loadScript.src = "https\://apis.google.com/js/client.js?onload=init" + forward.id + "1Picker"
    divElement.appendChild(loadScript);

    /*
    var divForDriveScriptForward = document.createElement("div")
    divForDriveScriptForward.id = "G" + elementNumber + "D" + i;
    divForDriveScriptForward.innerHTML = "<script>  \
    function initPicker() { \
      var picker = new FilePicker({ \
        apiKey: 'AIzaSyBrPcJgwBk7wZtCMpJ1Wz_AR_GlLQP1RGw',  \
        clientId: '23388632533-77bq0mev3uiumabgcl4r14ji10tk9687', \
        buttonEl: document.getElementById(\'" + forward.id + "\'), \
        onSelect: function(file) {  \
          console.log(file);  \
          alert('Selected ' + file.title); \
          document.getElementById(\'" + forwardLabel.id + "\').innerHTML=file.title;  \
        } \
      }); \
    } \
    </script>";
    divElement.appendChild(divForDriveScriptForward);
    */
    divElement.appendChild(document.createElement("br"));

    divElement.appendChild(document.createTextNode("Backward File:\t"));
    var backward = document.createElement("button");
    backward.id = "G" + elementNumber + "BB" + i;
    backward.innerHTML = "Select from Google Drive";
    divElement.appendChild(backward);

    var backwardLabel = document.createElement("label");
    backwardLabel.id = "G" + elementNumber + "BL" + i;
    divElement.appendChild(backwardLabel);

    var backwardScript = document.createElement("script")
    backwardScript.innerHTML = "function init" + backward.id + "2Picker() { \
      var picker = new FilePicker({ \
        apiKey: 'AIzaSyBrPcJgwBk7wZtCMpJ1Wz_AR_GlLQP1RGw',  \
        clientId: '23388632533-77bq0mev3uiumabgcl4r14ji10tk9687', \
        buttonEl: document.getElementById(\'" + backward.id + "\'), \
        onSelect: function(file) {  \
          console.log(file);  \
          document.getElementById(\'" + backwardLabel.id + "\').style.color=\"black\";  \
          document.getElementById(\'" + backwardLabel.id + "\').innerHTML=file.title;  \
          var fileJson = {};  \
          fileJson['fileid'] = file['id'];  \
          fileJson['parentid'] = file['parents'][0]['id'];  \
          fileJson['filename'] = file['title']; \
          fileUploadList['Group" + elementNumber + "']['Sample" + i + "']['Backward'] = fileJson;  \
        } \
      }); \
    }"
    divElement.appendChild(backwardScript);

    var loadScript1 = document.createElement("script");
    loadScript1.src = "https\://apis.google.com/js/client.js?onload=init" + backward.id + "2Picker"
    divElement.appendChild(loadScript1);

    /*
    var divForDriveScriptBackward = document.createElement("div")
    divForDriveScriptBackward.id = "G" + elementNumber + "D" + i;
    divForDriveScriptBackward.innerHTML = "<script>  \
    function initPicker() { \
      var picker = new FilePicker({ \
        apiKey: 'AIzaSyBrPcJgwBk7wZtCMpJ1Wz_AR_GlLQP1RGw',  \
        clientId: '23388632533-77bq0mev3uiumabgcl4r14ji10tk9687', \
        buttonEl: document.getElementById(\'" + backward.id + "\'), \
        onSelect: function(file) {  \
          console.log(file);  \
          alert('Selected ' + file.title); \
          document.getElementById(\'" + backwardLabel.id + "\').innerHTML=file.title;  \
        } \
      }); \
    } \
    </script>";
    divElement.appendChild(divForDriveScriptBackward);
    */
    divElement.appendChild(document.createElement("br"));
    divElement.appendChild(document.createElement("br"));
  }
}


function errorHandling() {
  var error = false;
  if(Object.keys(fileUploadList).length == 0) {
    document.getElementById('output').style.color = "red";
    document.getElementById('output').innerHTML = "Error: Nothing to submit.";
    return true;
  }
  for(var groupNumber = 0; groupNumber < Object.keys(fileUploadList).length; groupNumber++) {
    var groupIndex = 'Group' + groupNumber;
    if(Object.keys(fileUploadList[groupIndex]).length == 0) {
      document.getElementById('output').style.color = "red";
      document.getElementById('output').innerHTML = "Error: Group " + (groupNumber + 1) + " has no samples to submit.";
      return true;
    }
    for(var sampleNumber = 0; sampleNumber < Object.keys(fileUploadList[groupIndex]).length; sampleNumber++) {
      var sampleIndex = 'Sample' + sampleNumber;
      if(fileUploadList[groupIndex][sampleIndex]['Forward'] == null) {
        document.getElementById('G' + groupNumber + 'FL' + sampleNumber).style.color = "red";
        document.getElementById('G' + groupNumber + 'FL' + sampleNumber).innerHTML = "Error: Please choose a file";
        error = true;
      }
      if(fileUploadList[groupIndex][sampleIndex]['Backward'] == null) {
        document.getElementById('G' + groupNumber + 'BL' + sampleNumber).style.color = "red";
        document.getElementById('G' + groupNumber + 'BL' + sampleNumber).innerHTML = "Error: Please choose a file";
        error = true;
      }
    }
  }
  return error;
}

function upload() {
  //alert("submitted");
  document.getElementById('output').innerHTML = "";
  if(!errorHandling()) {
    var fps = document.getElementById('fps').value;
    var bps = document.getElementById('bps').value;
    var seqlen = document.getElementById('seqlen').value;
    var percent = document.getElementById('percent').value;
    var basecount = document.getElementById('basecount').value;

    var fd = new FormData();
    var jsondata = JSON.stringify(fileUploadList);
    fd.append('jsondata', jsondata);
    fd.append('fps', fps);
    fd.append('bps', bps);
    fd.append('seqlen', seqlen);
    fd.append('percent', percent);
    fd.append('basecount', basecount);

    $.ajax({
    url: '/upload',
    data: fd,
    processData: false,
    contentType: false,
    type: 'POST',
    success: function(data){
      alert(data);
      window.location.href = "/showform";
    }
    });
      //document.getElementById('output').style.color = "black";
      //var emailId = document.getElementById('email').value;
      //document.getElementById('output').innerHTML = JSON.stringify(fileUploadList) + '<br><br>' + emailId;
  }
}
/*
var clientId = '23388632533-77bq0mev3uiumabgcl4r14ji10tk9687.apps.googleusercontent.com';
var developerKey = 'AIzaSyBrPcJgwBk7wZtCMpJ1Wz_AR_GlLQP1RGw';
var accessToken;
function onApiLoad() {
  alert("onApiLoad");
  gapi.load('auth', authenticateWithGoogle);
  gapi.load('picker');
}
function authenticateWithGoogle() {
  window.gapi.auth.authorize({
    'client_id': clientId,
    'scope': ['https://www.googleapis.com/auth/drive.readonly'],
    'immediate': false
  }, handleAuthentication);
}
function handleAuthentication(result) {
  if(result && !result.error) {
    accessToken = result.access_token;
    setupPicker();
  }
}
function setupPicker() {
  var picker = new google.picker.PickerBuilder()
    .setOAuthToken(accessToken)
    .setDeveloperKey(developerKey)
    .addView(google.picker.ViewId.DOCUMENTS)
    .enableFeature(google.picker.Feature.NAV_HIDDEN)
    .setCallback(myCallback)
    .build();
  picker.setVisible(true);
}
function myCallback(data) {
  if (data.action == google.picker.Action.PICKED) {
    alert(data.docs[0].name);
  } else if (data.action == google.picker.Action.CANCEL) {
    alert('goodbye');
  }
}
*/
