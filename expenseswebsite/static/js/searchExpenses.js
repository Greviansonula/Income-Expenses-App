const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table")

tableOutput.style.display="none";

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

        
    if(searchValue.length > 0){
        fetch('/search-expenses', {
            body: JSON.stringify({ searchStr: searchValue }),
            method: "POST",
        })
        .then((res)=>res.json())
        .then((data)=>{
            console.log("data", data);

            // if(data.length == 0){
            //     console.log("data", data);
            // }
        });
    }
});