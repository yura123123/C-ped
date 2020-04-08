const testsList = document.getElementById("testsList");




document.getElementById("createTestButton").querySelector("input").addEventListener("click", () => createTest() );
document.getElementById("sendDataButton").addEventListener("click", sendData);


function sendData() {

}



function collectDataToJson() {
  data = new Object();
  data.searchRequest = document.getElementById("search").querySelector("textarea").value;
  data.tests = new Array();

  let testsCases = document.getElementById("testsList").getElementsByClassName("testCase");

  for (let testCase of testsCases) {
    let test = {
        "name": testCase.querySelector(".testName").querySelector("input").value,
        "result": testCase.querySelector(".testCaseResult").querySelector("input").value
    };

    test.arguments = new Array();
    testInputs = testCase.querySelector(".testCaseArgument").getElementsByTagName('input');
    for (let testInput of testInputs) {
      test.arguments.push(testInput.value);
    }
    data.tests.push(test);
  }
  return JSON.stringify(data);
}


function createArgument(button) {
  let argumentsWindow = button.parentNode.nextElementSibling.querySelector(".testCaseArgument");
  let input = document.createElement("input");
  input.setAttribute("type", "text");
  argumentsWindow.appendChild(input);
  input.focus();
  event.stopPropagation();

}

function toggleTestsWindow(test) {
  if (test.nextElementSibling.style.display == "none") {
    test.nextElementSibling.style.display = "block";
    test.querySelector(".addArgumentButton").style.display = "block";
  }
  else {
    test.nextElementSibling.style.display = "none";
    test.querySelector(".addArgumentButton").style.display = "none";
  }
}

function createTest() {
  let testsList = document.getElementById("testsList");

  let testCase = document.createElement("div");
  testCase.setAttribute("class", "testCase");

  let testName = document.createElement('div');
  testName.setAttribute('class', 'testName');
  testName.addEventListener("click", function () {
    toggleTestsWindow(this);
  });
  testCase.appendChild(testName);



  let testItem = document.createElement("div");
  testItem.setAttribute("class", "test");
  testCase.appendChild(testItem);
  testsList.appendChild(testCase);


  let testNameInput = document.createElement("input");
  testNameInput.setAttribute("type", "text");
  testName.appendChild(testNameInput);


  let addArgumentButton = document.createElement("input");
  addArgumentButton.setAttribute("src", "resources/btn2.png");
  addArgumentButton.setAttribute("type", "image");
  addArgumentButton.setAttribute("class", "addArgumentButton")
  addArgumentButton.addEventListener("click", function () {
    createArgument(this)
  });
  testName.appendChild(addArgumentButton);


  let wrapper = document.createElement("div");
  wrapper.setAttribute("class", "wrapper");
  testItem.appendChild(wrapper);

  let testCaseArgument = document.createElement('div');
  testCaseArgument.setAttribute("class", "testCaseArgument");
  testCaseArgument.innerHTML = "<span>"+ "argument" +"</span>";
  wrapper.appendChild(testCaseArgument);

  let testCaseResult = document.createElement('div');
  testCaseResult.setAttribute("class", "testCaseResult");
  testCaseResult.innerHTML = "<span>"+ "result" +"</span>";

  let resultInput = document.createElement("input");
  resultInput.setAttribute("type", "text");
  testCaseResult.appendChild(resultInput);

  wrapper.appendChild(testCaseResult);

  testNameInput.focus();
}
