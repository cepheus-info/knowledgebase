
import axios from 'axios';

export default async function getCapacity(city) {
    let result = await axios.get(`https://jsonmock.hackerrank.com/api/countries?name=${city}`);

    return result.data.data[0] && result.data.data[0].capital || '-1';
}