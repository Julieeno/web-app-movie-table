const myPromise = {
  then(resolve, reject) {
    setTimeout(function myFunction() {
      if (Math.random() < 0.2) {
        resolve("Success!");
      } else {
        reject("failure. Try again");
        myPromise.then(resolve, reject);
      }
    }, 2000)
  }
};



function resolve(str) {
  console.log(str);
}

function reject(str) {
  console.log(str);
}

myPromise
  .then(resolve, reject);