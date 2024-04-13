import axios from "axios";

process.env.REACT_APP_SERVER_API = process.env.REACT_APP_SERVER_API ?? ''

export const uploadFile = (file) => {
  const formdata = new FormData();
  formdata.append("file", file, file.fileName);

  const requestOptions = {
    method: 'POST',
    body: formdata,
    redirect: 'follow'
  };

  return fetch(`${process.env.REACT_APP_SERVER_API}/api/upload`, requestOptions)
    .then((res) => {
      return res.text()
    });
}

export const getModel = (id) => {
  return axios.post(`${process.env.REACT_APP_SERVER_API}/api/upload/${id}/result`)
    .then((res) => res.data);
}

export const getStatus = (id) => {
  return axios.post(`${process.env.REACT_APP_SERVER_API}/api/upload/${id}/status`)
    .then((res) => {
      if (res.status === 404) {
        throw new Error('Not found');
      }

      return res.data;
    });
}