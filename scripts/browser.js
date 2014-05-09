function onClickDirEntry(entryName)
{
	document.getElementById("path").innerHTML= "Changing to '"  + entryName + "'directory...";
	document.getElementById("listing").innerHTML= "Please wait...";
	if(window.XMLHttpRequest)
  	{// code for IE7+, Firefox, Chrome, Opera, Safari
  		xmlhttp=new XMLHttpRequest();
  	}
	else
  	{// code for IE6, IE5
  		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  	}
  	
  	xmlhttp.onreadystatechange=function()
  	{
  		if (xmlhttp.readyState==4 && xmlhttp.status==200)
    	{
    		document.getElementById("dir_view").innerHTML=xmlhttp.responseText;
    	}
  	};
  	
	xmlhttp.open("GET","cd_js?path=" + entryName, true);
	xmlhttp.send();
}

function onClickDeleteEntry(entryName)
{
	if (!confirm("Are you sure you want to delete '"  + entryName + "'?"))
	{
		return;
	}
	document.getElementById("path").innerHTML= "Deleting file '"  + entryName + "'...";
	document.getElementById("listing").innerHTML= "Please wait...";
	if(window.XMLHttpRequest)
  	{// code for IE7+, Firefox, Chrome, Opera, Safari
  		xmlhttp=new XMLHttpRequest();
  	}
	else
  	{// code for IE6, IE5
  		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  	}
  	
  	xmlhttp.onreadystatechange=function()
  	{
  		if (xmlhttp.readyState==4 && xmlhttp.status==200)
    	{
    		document.getElementById("dir_view").innerHTML=xmlhttp.responseText;
    	}
  	};
  	
	xmlhttp.open("GET","delete_js?dirEntry=" + entryName, true);
	xmlhttp.send();
}

function showUploadView()
{
	document.getElementById("upload-form").style.display = "block";
	document.getElementById("upload-button").style.display = "none";
}

function hideUploadView()
{
	document.getElementById("upload-form").style.display = "none";
	document.getElementById("upload-button").style.display = "block";
}

function showNewFolderForm()
{
	document.getElementById("new-folder-form").style.display = "block";
	document.getElementById("new-folder-button").style.display = "none";
  	document.getElementById("new-folder-name").focus();
}

function hideNewFolderForm()
{
	document.getElementById("new-folder-form").style.display = "none";
	document.getElementById("new-folder-button").style.display = "block";
}

function onClickFileName(dirEntry)
{
	if(window.XMLHttpRequest)
  	{// code for IE7+, Firefox, Chrome, Opera, Safari
  		xmlhttp=new XMLHttpRequest();
  	}
	else
  	{// code for IE6, IE5
  		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  	}
  	
  	xmlhttp.onreadystatechange=function()
  	{
  		if (xmlhttp.readyState==4 && xmlhttp.status==200)
    	{
    		document.getElementById("file_" + dirEntry).innerHTML=xmlhttp.responseText;
 		  	document.getElementById("file_" + dirEntry + "_newname").focus();
   	}
  	};
  	
	xmlhttp.open("GET","rename_view_js?dirEntry=" + dirEntry, true);
	xmlhttp.send();
}

function genNewFileNameSpan(dirEntry)
{
	return "<span onclick=\"onClickFileName('" + dirEntry + "')\">" + dirEntry + "</span>";
}

function cancelRename(dirEntry)
{
	document.getElementById("file_" + dirEntry).innerHTML=genNewFileNameSpan(dirEntry);
}

function onRenameEntry(dirEntry)
{
	if(window.XMLHttpRequest)
  	{// code for IE7+, Firefox, Chrome, Opera, Safari
  		xmlhttp=new XMLHttpRequest();
  	}
	else
  	{// code for IE6, IE5
  		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  	}
  	
  	xmlhttp.onreadystatechange=function()
  	{
  		if (xmlhttp.readyState==4 && xmlhttp.status==200)
    	{
    		div = document.getElementById("file_" + dirEntry); 
    		div.innerHTML=genNewFileNameSpan(xmlhttp.responseText);
    		div.setAttribute("id", "file_" + xmlhttp.responseText);
    	}
  	};
  	
  	newName = document.getElementById("file_" + dirEntry + "_newname").value;
  	
	xmlhttp.open("GET","rename_js?dirEntry=" + dirEntry + "&newName=" + newName, true);
	xmlhttp.send();
}

function createFolder(folderName)
{
	if(window.XMLHttpRequest)
  	{// code for IE7+, Firefox, Chrome, Opera, Safari
  		xmlhttp=new XMLHttpRequest();
  	}
	else
  	{// code for IE6, IE5
  		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  	}
  	
  	xmlhttp.onreadystatechange=function()
  	{
  		if (xmlhttp.readyState==4 && xmlhttp.status==200)
    	{
    		document.getElementById("dir_view").innerHTML=xmlhttp.responseText;
    	}
  	};
  	
  	newName = document.getElementById("new-folder-name").value;
  	
	xmlhttp.open("GET", "mkdir_js?newName=" + newName, true);
	xmlhttp.send();
}
