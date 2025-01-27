import * as React from "react";

const useVisibilityChangeSubscribe = (callback) => {
  document.addEventListener("visibilitychange", callback);
  return () => {
    document.removeEventListener("visibilitychange", callback);
  };
};

const getVisibilityChangeSnapshot = () => {
  return document.visibilityState;
};

const getVisibilityChangeServerSnapshot = () => {
  throw Error("useVisibilityChange is a client-only hook");
};

/**
 * Custom React hook to respond to the document's 'visibilitychange'
 * event with useEffect. Returns reactive value boolean value
 * tracking the document's visibilityState property.
 */
export function useVisibilityChange() {
  const visibilityState = React.useSyncExternalStore(
    useVisibilityChangeSubscribe,
    getVisibilityChangeSnapshot,
    getVisibilityChangeServerSnapshot,
  );

  return visibilityState === "visible";
}

/**
 * Custom React hook for performing an external API call
 * on an interval in microseconds.
 * @param {function} apiFunction - external function call
 * @param {number} delay - interval timer in microseconds
 */
export function useApiPolling(apiFunction, delay) {
  const [data, setData] = React.useState(null);

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await apiFunction();
        setData(response);
      } catch (error) {
        console.log(error);
      }
    };

    const intervalId = setInterval(fetchData, delay);

    // Clear the interval on unmount
    return () => clearInterval(intervalId);
  }, [apiFunction, delay]);

  return data;
}
