window.currentVolumeObject = "";
window.currentVolumeKey = "";
window.currentChapter = -1;

window.loadVolumes = function() {
	$("#navigationholder").empty();

	// deal with the breadcrumbs
	$("#breadcrumb").empty();
	crumbString = "<li><a href='javascript:loadVolumes();'>  Scriptures  </a><span class='divider'>/</span></li>";
	$("#breadcrumb").append(crumbString);

	$.each(window.volumesObjects, function(key, value) {
		keyString = '"'+key+'"';
		string = "<a href='javascript:loadBooks(" + keyString + ");'>"
				+ value.volume_title + "</a><br>";
		$("#navigationholder").append(string);
	});
}

window.loadBooks = function(volumeKey) {
	$("#navigationholder").empty();

	currentVolumeObject = window.volumesObjects[volumeKey];
	currentVolumeKey = volumeKey;

	// deal with the breadcrumbs
	$("#breadcrumb").empty();
	crumbString1 = "<li><a href='javascript:loadVolumes();'>  Scriptures </li>";
	keyString = '"'+currentVolumeKey+'"';
	crumbString2 = "<li><a href='javascript:loadBooks(" + keyString + ");'>  "
			+ currentVolumeObject.volume_title + " </li>";
	$("#breadcrumb").append(crumbString1);
	$("#breadcrumb").append(crumbString2);

	// the json array of books for the selected volume
	$.each(currentVolumeObject.books, function(key, value) {
		volKeyString = '"'+currentVolumeKey+'"';
		bookKeyString = '"'+key+'"';
		string = "<a href='javascript:loadChapters(" + volKeyString + ", "+ bookKeyString +");'>"
				+ value.book_title + "</a><br>";
		$("#navigationholder").append(string);
	});

}

window.loadChapters = function(volumeKey, bookKey) {
	$("#navigationholder").empty();
	currentVolumeObject = window.volumesObjects[volumeKey];
	currentVolumeKey = volumeKey;
	
	currentBookObject = currentVolumeObject.books[bookKey];
	currentBookKey = bookKey;

	// deal with the breadcrumbs
	$("#breadcrumb").empty();
	crumbString1 = "<li><a href='javascript:loadVolumes();'>  Scriptures </li>";
	keyString = '"'+currentVolumeKey+'"';
	crumbString2 = "<li><a href='javascript:loadBooks(" + keyString + ");'>  "
		+ currentVolumeObject.volume_title + " </li>";
	
	volKeyString = '"'+currentVolumeKey+'"';
	bookKeyString = '"'+currentBookKey+'"';
	crumbString3 = "<li><a href='javascript:loadChapters(" + volKeyString + ", "+ bookKeyString +");'>  " + currentBookObject.book_title + " </li>";
	$("#breadcrumb").append(crumbString1);
	$("#breadcrumb").append(crumbString2);
	$("#breadcrumb").append(crumbString3);

	chapterString = "";
	for ( var i = 0; i < currentBookObject.num_chapters; i++) {
		displayNum = i + 1;
		string = " <a href='javascript:loadVerses(" + volKeyString + ", "+ bookKeyString +", " + i + ");'>" + displayNum
				+ "</a>   -";
		chapterString += string;
	}
	chapterString = chapterString.slice(0, -1);
	$("#navigationholder").append(chapterString);

}

window.loadVerses = function(volumeKey, bookKey, chapterNum) {
	$("#navigationholder").empty();
	currentVolumeObject = window.volumesObjects[volumeKey];
	currentVolumeKey = volumeKey;
	
	currentBookObject = currentVolumeObject.books[bookKey];
	currentBookKey = bookKey;

	// deal with the breadcrumbs
	$("#breadcrumb").empty();
	crumbString1 = "<li><a href='javascript:loadVolumes();'>  Scriptures </li>";
	keyString = '"'+currentVolumeKey+'"';
	crumbString2 = "<li><a href='javascript:loadBooks(" + keyString + ");'>  "
		+ currentVolumeObject.volume_title + " </li>";
	
	volKeyString = '"'+currentVolumeKey+'"';
	bookKeyString = '"'+currentBookKey+'"';
	crumbString3 = "<li><a href='javascript:loadChapters(" + volKeyString + ", "
		+ bookKeyString +");'>  " 
		+ currentBookObject.book_title 
		+ " </li>";
	chapterInt = parseInt(chapterNum)+1
	crumbString4 = "<li> " + chapterInt + " </li>";
	$("#breadcrumb").append(crumbString1);
	$("#breadcrumb").append(crumbString2);
	$("#breadcrumb").append(crumbString3);
	$("#breadcrumb").append(crumbString4);

	$.getJSON($SCRIPT_ROOT + '/get_verses', {
		book : currentBookObject.book_id,
		chapter_id : parseInt(chapterNum) + 1
	}, function(data) {
		$("#navigationholder").empty();
		$.each(data, function() {
			// alert('data ' +
			// this.verse_scripture);
			scriptureString = "<div " + "onmouseover='verseMouseOver(this)' "
					+ "onmouseout='verseMouseOut(this)' "
					+ "onclick='verseClick(this)' >" + this.verse + ". "
					+ this.verse_scripture + "</div><br>"
			$("#navigationholder").append(scriptureString);
		});
	});
}

window.verseClick = function(div) {
	alert('mouse over ' + div);
	div.style.backgroundColor = '#cccccc';
}

window.verseMouseOver = function(div) {
	// alert('mouse over ' + div);
	div.style.backgroundColor = '#cccccc';
	div.style.cursor = "pointer"
}

window.verseMouseOut = function(div) {
	// alert('mouse over ' + div);
	div.style.backgroundColor = 'white';
}

// the on ready function
$(document).ready(function() {
	if (chapter_num != "None" && book_name != "None" && volume_name != "None") {
		chapterInt = parseInt(chapter_num)-1;
		loadVerses(volume_name, book_name, chapterInt);
	} else if (book_name != "None" && volume_name != "None") {
		loadChapters(volume_name, book_name);
	}else if (volume_name != "None") {
		loadBooks(volume_name);
	} else {
		loadVolumes();
	}
});
