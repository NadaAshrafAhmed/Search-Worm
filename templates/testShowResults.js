chrome.storage.local.get('res',function(item){

    if(item['res'])
    {
        window.opener.document.getElementById('showResults').value="true";

        for(var i=1;i<=4;i++)
        {
            var ls=document.getElementById('res'+i).getElementsByTagName('a');
            for(var j=0;j<ls.length;j++)
            {

                if(!item['res'][i-1].find(function(element) {
                  return element == ls[j].innerHTML;}))
                {
                    window.opener.document.getElementById('showResults').value="false";
                    console.log("err");
                    break;
                }
            }
        }
    }
});