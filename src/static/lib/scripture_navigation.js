currentVolumeBookArray = "";
currentVolumeObject = "";
currentVolumeKey = "";
currentChapter = -1;

function loadVolumes() {
	$("#holder").empty();

	// deal with the breadcrumbs
	$("#breadcrumb").empty();
	crumbString = "<li><a href='javascript:loadVolumes();'>  Scriptures  </a><span class='divider'>/</span></li>";
	$("#breadcrumb").append(crumbString);

	$.each(volumesArray, function(key, value) {
		string = "<a href='javascript:loadBooks(" + key + ");'>"
				+ value.volume_title + "</a><br>";
		$("#holder").append(string);
	});
}



function loadBooks(volumeKey) {
	$("#holder").empty();

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
		$("#holder").append(string);
	});

}

function loadChapters(bookKey) {
	$("#holder").empty();

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
	$("#holder").append(chapterString);
	
}

function loadVerses(chapterNum){
	$.getJSON($SCRIPT_ROOT + '/get_verses', {
		book : currentBookObject.book_id,
		chapter_id : chapterNum+1
	}, function(data) {
		$("#holder").empty();
		$.each(data, function(){
//			alert('data ' + this.verse_scripture);
			scriptureString = "<p>"+this.verse+". "+this.verse_scripture+"</p>"
			$("#holder").append(scriptureString);
		});
	});
}


// the on ready function
$(document).ready(function() {
	loadVolumes();
});