$.get("/get_registered_schools", function(data){
  for (let i in data){
      var str = data[i];
      var url = "/"+ data[i];
    	$("#notfound").append(`<a style="color: black;" href="${url}"><center>${str}</center></a><br>` );
    }
});
