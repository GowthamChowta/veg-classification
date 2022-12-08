import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { Fab } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import Button from '@mui/material/Button';
import LoadingButton from '@mui/lab/LoadingButton';
import axios from 'axios';

const URL1 = 'http://34.171.107.1:5000/predict';

function App() {
  const [model, setModel] = useState('');
  const [loading, setIsLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<any>();
  const [result, setResult] = useState('');

  const handleChange = (event: SelectChangeEvent) => {
    setModel(event.target.value as string);
  };
  const handleFileUpload = (event: any) => {
    setSelectedFile(event.target.files[0]);
    setResult('');
  };

  const inferenceModel = () => {
    let data = new FormData();
    data.append('image', selectedFile as any);
    data.append('modelParam', model);

    setIsLoading(true);
    axios
      .post(URL1, data, {
        headers: {
          'Content-Type': `multipart/form-data`,
        },
      })
      .then(response => {
        console.log(response);
        setResult(response.data);
        setIsLoading(false);
      })
      .catch(error => {
        console.log(error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  console.log('File name is', selectedFile);

  return (
    <div>
      <div className="vegetable-classification">
        <div className="vegetable-cls-container">
          <div className="title">
            <h3>Vegetable Image Classification</h3>
          </div>
          <div className="formfield">
            <InputLabel id="model">Model</InputLabel>
            <div className="dropdown">
              <Select
                labelId="model"
                id="demo-simple-select"
                value={model}
                label="Model"
                onChange={handleChange}
                sx={{ width: 150 }}>
                <MenuItem value={'VGG16'}>VGG</MenuItem>
                <MenuItem value={'ResNet'}>ResNet</MenuItem>
                <MenuItem value={'MobileNet'}>MobileNet</MenuItem>
              </Select>
            </div>
          </div>
          <label htmlFor="upload-photo" className="upload-photo formfield">
            <input
              style={{ display: 'none' }}
              id="upload-photo"
              name="upload-photo"
              type="file"
              onChange={handleFileUpload}
            />
            <div className="upload-photo-button">
              <Fab color="secondary" size="small" component="span" aria-label="add" variant="extended">
                <AddIcon /> {!selectedFile ? 'Upload Photo' : 'Re-Upload photo'}
              </Fab>
            </div>
            <div className="uploaded-photo">
              {selectedFile && <div className="keepDistant">Uploaded: {selectedFile.name}</div>}
              {selectedFile && (
                <div className="keepDistant">
                  {<img src={URL.createObjectURL(selectedFile)} width={190} height={190}></img>}
                </div>
              )}
            </div>
          </label>
          <div className="formfield">
            <LoadingButton
              loading={loading}
              loadingPosition="start"
              variant="contained"
              onClick={inferenceModel}
              sx={{ width: '140px' }}>
              Predict
            </LoadingButton>
          </div>
          {result && (
            <div className="rainbow">
              <Results result={result} />
            </div>
          )}
        </div>
      </div>

      <Footer />
    </div>
  );
}

const Footer = () => {
  return (
    <div className="footer">
      <ul className="footerul">
        <li>
          <a href="https://www.linkedin.com/in/sri-rashmitha-boya/">Rashmitha</a>
        </li>
        <li>
          <a href="https://www.linkedin.com/in/shyam-kumar-kanuru/">Shyam Kumar</a>
        </li>
        <li>
          <a href="https://www.linkedin.com/in/ritwik-budhiraja-38193b182/">Ritwik</a>
        </li>
        <li>
          <p>👋</p>
        </li>
      </ul>
    </div>
  );
};

export const Results = ({ result }: any) => {
  return (
    <div className="results">
      {result && (
        <div>
          <div className="results-title">Predicted Class: </div>
          <div className="results-title">{result}</div>
        </div>
      )}
    </div>
  );
};

export default App;
