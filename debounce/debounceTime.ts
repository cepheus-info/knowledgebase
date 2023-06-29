
function debounceTime(callback, wait) {
    // declare timeout variable
    let timeout;
    // return a function
    return (...x) => {
        // if timeout is set, clear it
        if (timeout) clearTimeout(timeout);
        // set timeout to a new timeout
        timeout = setTimeout(() => {
            // call the callback with the arguments
            callback.call(arguments.callee, ...x);
        }, wait);
    }
}

// call debounce function
const func = debounceTime((x, y, z) => console.log(x, y, z), 1000);
func(1, 2, 3, 4);
func(2, 1, 3, 5);