function getFile(){
    document.getElementById("file1").click();
  }
  function sub(obj){
     var file = obj.value;
     var fileName = file.split("\\");
     let filx=document.getElementById("yourBtn");
     filx.innerHTML = fileName[fileName.length-1];
     filx.className="btn-CHS fontCHG";
   }