
export function debounce(callback, wait) {
    let timeout;
    return () => {
        if (timeout) clearTimeout(timeout);
        timeout = setTimeout(() => {
            callback.call(arguments.callee, arguments);
        }, wait);
    };
}

// call debounce function
const func = debounce(() => console.log('hello'), 1000);
func();
func();