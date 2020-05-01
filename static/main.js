const MAX_NUM_COLUMNS = 4;

if(urlParams.get("sent_message")){
  $.notify("You successfully sent a message", "success");
}

function afterSpace(full_name){
  return full_name.substring(full_name.indexOf(" ")+1);
}

$.get("/getProfiles", function(data){
    let allRows = [];

    let currentRow = [];
    let ct = 0;

    let ppl_uuids = Object.keys(data);
    ppl_uuids.sort((a,b)=>{
        if( afterSpace(data[a].name) < afterSpace(data[b].name) ){
	    return -1;
	}
	else {
	    return 1;
	}
    });
    for(let i in ppl_uuids){
	uuid = ppl_uuids[i];
      if(ct % MAX_NUM_COLUMNS == 0 && ct != 0){
        allRows.push(currentRow);
        currentRow = [];
      }
      let link = `/sendmessages?sendto=${uuid}`;
      let currentCard = $(`<div class='face-card' id="card_${uuid}" onclick='window.location.href="${link}"'></div>`);
      currentCard.append($(`<img id="img_${uuid}" alt="profile picture missing" src="${pfp_path}/${uuid}.png" height="50%" onerror="this.onerror=null;this.src='${pfp_path}/panda.png';"></img>`));
      let nameText = $(`<h2 id="my${uuid}" style="font-size:2.5vw"></h2>`);
      nameText.text(data[uuid].name);
      currentCard.append(nameText);
      let bioText = $(`<p id="bio${uuid}"></p>`)
      bioText.text(data[uuid].bio);
      currentCard.append(bioText);
      currentRow.push(currentCard);
      ct++;
    }
    while(ct % MAX_NUM_COLUMNS != 0){
      ct++;
      currentRow.push($("<div class='col-sm face-card'></div>"));
    }
    allRows.push(currentRow);

    for(let i = 0; i < MAX_NUM_COLUMNS; i++){
      let currentColumn = $("<div class='column'></div>");
      for (row in allRows){
        currentColumn.append(allRows[row][i]);
      }
      $("#faces").append(currentColumn);
    }
});

var cw = $(".face-card").width();
$(".face-card").css({
    'height': cw + 'px'
});

$.get("/get_uuids_sentto", (uuids_sentto)=>{
    for(let i in uuids_sentto){
        document.getElementById("my" + uuids_sentto[i]).innerHTML += "&#x2713"; // checkmark
    }
});

function search_name(){
  let name = $("#search").val();
  if(name){
    let img_elt = document.getElementById("img_"+name);
    if(img_elt)
      img_elt.scrollIntoView();
  }
}

/*
//temporarily diable search bar
document.getElementById("search").addEventListener("keyup", function(event){
  if(event.keyCode=== 13){
    event.preventDefault();
    search_name();
  }
});
*/
