function showResults(){
    chrome.storage.local.get('res',function(results){
        if(results['res']){

            for (var k=1;k<=results['res'].length;k++) // loop 3al 4 arrays bto3 al result urls
            {
                i=results['res'][k-1]; // i=topic[i] list of urls
                var ind=[];
                for (var j=0;j<i.length;j++)// ind=[0,1,2,3,...,len(topic[i])]
                {
                    ind.push(j);
                }
                var ul = document.getElementById("res"+k); // get card for topic[i] in html
                for(var j=0;j<Math.min(5,i.length);j++)
                {
                    var chosen=Math.floor(Math.random() * ind.length) // choose random index

                    var li = document.createElement("li");
                    var a = document.createElement("a");
                    a.appendChild(document.createTextNode(i[ind[chosen]])); // put the url of chosen random index in the card
                    a.setAttribute("href", i[ind[chosen]]);
                    a.setAttribute("class", "card-link");

                    li.appendChild(a);
                    ul.appendChild(li);
                    ind.splice(chosen,1);// remove chosen url index
                }
            }
            document.getElementById("content").style.visibility="visible";
        }
        else{

        //show defult res
        }
    });
}