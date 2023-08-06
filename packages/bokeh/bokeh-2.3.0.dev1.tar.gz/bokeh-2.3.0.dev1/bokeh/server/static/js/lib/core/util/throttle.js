var _a, _b, _c, _d;
function _delay_animation(callback) {
    callback(Date.now()); // XXX: performance.now()
    return -1;
}
const delay_animation = (_d = (_c = (_b = (_a = (typeof window !== 'undefined' ? window.requestAnimationFrame : undefined)) !== null && _a !== void 0 ? _a : (typeof window !== 'undefined' ? window.webkitRequestAnimationFrame : undefined)) !== null && _b !== void 0 ? _b : (typeof window !== 'undefined' ? window.mozRequestAnimationFrame : undefined)) !== null && _c !== void 0 ? _c : (typeof window !== 'undefined' ? window.msRequestAnimationFrame : undefined)) !== null && _d !== void 0 ? _d : _delay_animation;
// Returns a function, that, when invoked, will only be triggered at
// most once during a given window of time.
//
// In addition, if the browser supports requestAnimationFrame, the
// throttled function will be run no more frequently than request
// animation frame allows.
//
// @param func [function] the function to throttle
// @param wait [number] time in milliseconds to use for window
// @return [function] throttled function
//
export function throttle(func, wait) {
    let timeout = null;
    let previous = 0;
    let pending = false;
    return function () {
        return new Promise((resolve, reject) => {
            const later = function () {
                previous = Date.now();
                timeout = null;
                pending = false;
                try {
                    func();
                    resolve();
                }
                catch (error) {
                    reject(error);
                }
            };
            const now = Date.now();
            const remaining = wait - (now - previous);
            if (remaining <= 0 && !pending) {
                if (timeout != null) {
                    clearTimeout(timeout);
                }
                pending = true;
                delay_animation(later);
            }
            else if (!timeout && !pending) {
                timeout = setTimeout(() => delay_animation(later), remaining);
            }
            else {
                resolve();
            }
        });
    };
}
//# sourceMappingURL=throttle.js.map