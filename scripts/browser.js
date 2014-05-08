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
    		document.getElementById("upload").innerHTML=xmlhttp.responseText;
    	}
  	};
  	
	xmlhttp.open("GET","show_upload_js", true);
	xmlhttp.send();
}

function hideUploadView()
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
    		document.getElementById("upload").innerHTML=xmlhttp.responseText;
    	}
  	};
  	
	xmlhttp.open("GET","hide_upload_js", true);
	xmlhttp.send();
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
  	
	xmlhttp.open("GET","rename_js?dirEntry=" + dirEntry + '&newName=' + newName, true);
	xmlhttp.send();
}
