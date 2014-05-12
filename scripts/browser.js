function displayPleaseWait(message)
{
	document.getElementById("path").innerHTML = message;
	document.getElementById("listing").innerHTML = message;
}

function onClickDirEntry(entryName)
{
	var cdTimeOut = setTimeout(function(){displayPleaseWait("Please wait. Changing to '"  + entryName + "' directory...");}, 250);
	
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
    		window.clearTimeout(cdTimeOut);
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

	var cdTimeOut = setTimeout(function(){document.getElementById("entry_" + entryName).innerHTML = "Please wait, deleting entry...";}, 250);
	
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
    		window.clearTimeout(cdTimeOut);
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

function onClickFileName(dirEntry, isdir)
{
	document.getElementById("file_" + dirEntry).innerHTML = "Please wait...";
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
    		if (isdir)
    		{
	    		document.getElementById("link_" + dirEntry).onclick = function () {return false;};
    		}
    		document.getElementById("file_" + dirEntry).innerHTML=xmlhttp.responseText;
 		  	document.getElementById("file_" + dirEntry + "_newname").focus();
   		}
  	};
  	
	xmlhttp.open("GET","rename_view_js?dirEntry=" + dirEntry, true);
	xmlhttp.send();
}

function genNewFileNameSpan(dirEntry)
{
	return "<span onclick=\"onClickFileName('" + dirEntry + "', false)\">" + dirEntry + "</span>";
}

function cancelRename(dirEntry)
{
	document.getElementById("file_" + dirEntry).innerHTML=genNewFileNameSpan(dirEntry);
}

function onRenameEntry(dirEntry, isdir)
{
  	newName = document.getElementById("file_" + dirEntry + "_newname").value;
  	
	var cdTimeOut = setTimeout(function(){document.getElementById("entry_" + dirEntry).innerHTML = "Please wait, renaming file...";}, 250);
	
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
    		window.clearTimeout(cdTimeOut);
    		document.getElementById("dir_view").innerHTML=xmlhttp.responseText;
    	}
  	};
  	
	xmlhttp.open("GET","rename_js?dirEntry=" + dirEntry + "&newName=" + newName, true);
	xmlhttp.send();
}

function createFolder(folderName)
{
  	newName = document.getElementById("new-folder-name").value;
  	
	var cdTimeOut = setTimeout(function(){displayPleaseWait("Please wait. Creating folder '"  + newName + "'...");}, 250);
	
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
    		window.clearTimeout(cdTimeOut);
    		document.getElementById("dir_view").innerHTML=xmlhttp.responseText;
    	}
  	};
  	
	xmlhttp.open("GET", "mkdir_js?newName=" + newName, true);
	xmlhttp.send();
}
