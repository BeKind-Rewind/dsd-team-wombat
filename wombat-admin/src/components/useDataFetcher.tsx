import { useState, useEffect } from 'react';

const useDataFetcher = (url: string, filterFn?: any) => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const responseData = await response.json();
                if (filterFn) {
                    setData(filterFn(responseData))
                }
                else {
                    setData(responseData)
                }

            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
    }, [url, filterFn]);

    return data;
};

export default useDataFetcher;