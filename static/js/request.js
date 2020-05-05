$.get("/view_my_request", function(data){
  if(data == "no requests"){
    $.notify("no requests yet");
  }
  else{
  	for(let i in data){
  		person = data[i];
  		$("#request").append(`<center>${person}<br></center>`);
  	}
  }
});

/*

$.get("/get_uuid", function(uuid){
  $.get("/view_profile", {"uuid": uuid}, function(data){
    let currentCard = $("<div class='face-card' style='height:auto'></div>");
    currentCard.append($(`<img id="img_${uuid}" alt="profile picture missing" src="${pfp_path}/${uuid}.png" onerror="this.onerror=null;this.src='${assets_path}/panda.png';"></img>`));

    let nameText = $("<h2></h2>");
    nameText.text(data.name);
    currentCard.append(nameText);

    let bioText = $("<p></p>");
    bioText.text(data.bio);
    currentCard.append(bioText);
    $("#myprofile").append(currentCard);
  });
});

$.get("/view_my_request", function(data){
  if(data == "no requests"){
    $.notify("no requests yet");
  }
  else{
	for(let sender_person in data){
		person = data[sender_person];
		$("#request").append(${person});
	}
  }
});

*/