window.currentVolumeBookArray = "";
window.currentVolumeObject = "";
window.currentVolumeKey = "";
window.currentChapter = -1;

window.loadVolumes = function() {
	$("#navigationholder").empty();

	// deal with the breadcrumbs
	$("#breadcrumb").empty();
	crumbString = "<li><a href='javascript:loadVolumes();'>  Scriptures  </a><span class='divider'>/</span></li>";
	$("#breadcrumb").append(crumbString);

	$.each(volumesArray, function(key, value) {
		string = "<a href='javascript:loadBooks(" + key + ");'>"
				+ value.volume_title + "</a><br>";
		$("#navigationholder").append(string);
	});
}



window.loadBooks = function(volumeKey) {
	$("#navigationholder").empty();

	currentVolumeObject = volumesArray[volumeKey];
	currentVolumeKey = volumeKey;

	// deal with the breadcrumbs
	$("#breadcrumb").empty();
	crumbString1 = "<li><a href='javascript:loadVolumes();'>  Scriptures </li>";
	crumbString2 = "<li><a href='javascript:loadBooks(" + volumeKey + ");'>  "
			+ currentVolumeObject.volume_title + " </li>";
	$("#breadcrumb").append(crumbString1);
	$("#breadcrumb").append(crumbString2);

	// the json array of books for the selected volume
	currentVolumeBookArray = eval(currentVolumeObject.book_key)
	$.each(currentVolumeBookArray, function(key, value) {
		string = "<a href='javascript:loadChapters(" + key + ");'>"
				+ value.book_title + "</a><br>";
		$("#navigationholder").append(string);
	});

}

window.loadChapters = function(bookKey) {
	$("#navigationholder").empty();

	currentBookObject = currentVolumeBookArray[bookKey];
	currentBookKey = bookKey;

	// deal with the breadcrumbs
	$("#breadcrumb").empty();
	crumbString1 = "<li><a href='javascript:loadVolumes();'>  Scriptures </li>";
	crumbString2 = "<li><a href='javascript:loadBooks(" + currentVolumeKey
			+ ");'>  " + currentVolumeObject.volume_title + " </li>";
	crumbString3 = "<li><a href='javascript:loadChapters(" + currentBookKey
			+ ");'>  " + currentBookObject.book_title + " </li>";
	$("#breadcrumb").append(crumbString1);
	$("#breadcrumb").append(crumbString2);
	$("#breadcrumb").append(crumbString3);

	chapterString = "";
	for ( var i = 0; i < currentBookObject.num_chapters; i++) {
		displayNum = i + 1;
		string = " <a href='javascript:loadVerses("+i+");'>" + displayNum + "</a>   -";
		chapterString += string;
	}
	chapterString = chapterString.slice(0,-1);
	$("#navigationholder").append(chapterString);

}

window.verseMouseOver = function(div){
//	alert('mouse over ' + div);
	div.style.backgroundColor = 'green';
}

window.verseMouseOut = function(div){
//	alert('mouse over ' + div);
	div.style.backgroundColor = 'white';
}

window.loadVerses = function(chapterNum){
	// deal with the breadcrumbs
	$("#breadcrumb").empty();
	crumbString1 = "<li><a href='javascript:loadVolumes();'>  Scriptures </li>";
	crumbString2 = "<li><a href='javascript:loadBooks(" + currentVolumeKey
			+ ");'>  " + currentVolumeObject.volume_title + " </li>";
	crumbString3 = "<li><a href='javascript:loadChapters(" + currentBookKey
			+ ");'>  " + currentBookObject.book_title + " </li>";
	crumbString4 = "<li> " + chapterNum + " </li>";
	$("#breadcrumb").append(crumbString1);
	$("#breadcrumb").append(crumbString2);
	$("#breadcrumb").append(crumbString3);
	$("#breadcrumb").append(crumbString4);
	
	$.getJSON($SCRIPT_ROOT + '/get_verses', {
		book : currentBookObject.book_id,
		chapter_id : chapterNum+1
	}, function(data) {
		$("#navigationholder").empty();
		$.each(data, function(){
//			alert('data ' + this.verse_scripture);
			scriptureString = "<div onmouseover='verseMouseOver(this)' onmouseout='verseMouseOut(this)'><p>"+this.verse+". "+this.verse_scripture+"</p></div>"
			$("#navigationholder").append(scriptureString);
		});
	});
}


// the on ready function
$(document).ready(function() {
	loadVolumes();
});
