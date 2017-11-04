const express = require('express');
const router = express.Router();
const python = require('python-shell');
var path = '/Users/bttb66/Documents/ariano/ariano/nmf/python_speech_features-master/butterfly.wav';
const multer = require('multer');
var filename = '';
const storage = multer.diskStorage({
    destination: './public/music',
    filename: function (req, file, cb) {
        filename = file.fieldname + '-' + Date.now();
        cb(null, filename);
    }
});
const upload = multer({storage : storage});


router.post('/', upload.single('music'), (req, res) => {
    try {
	console.log('score 시작');
      if(!req.file.path || !req.body.song){
        res.status(403).send({"message" : "Please input all of song, music."})
      }else{
        var option = {
            mode: 'text',
            pythonPath: '/usr/bin/python',
            pythonOptions: ['-u'],
            scriptPath: __dirname,
            args: [req.file.path, req.body.song]
        };
	console.log('score 들어옴',req.file.path);
        python.run('pitch.py', option, function (err, result) {
            if (err) {
              console.log('Something Gone Wrong!', err);
              res.status(500).send({"message": "syntax err" });
            } else{
              console.log('result is : ', result);
              res.status(200).send({ "message" : "success", "result" : parseInt(result[0]) });
            }
        });
      }
    } catch (err) {
        console.log('err msg: ', err);
        res.status(500).send({ "message": "syntax err" });
    } finally {
    }
});


router.get('/test', (req, res)=>{
    try{
        var option = {
            mode: 'text',
            pythonPath: '',
            pythonOptions: ['-u'],
            scriptPath: '',
            args: ['I', 'am', 'full']
        };
        python.run('./pylib/test.py', option, function (err, result) {
            if (err) {
                console.log('Something Gone Wrong!', err);
            }
            console.log('result is : ', result);
            res.status(200).send({ "result": "test" });
        });
    } catch(err){
        console.log('err msg: ', err);
        res.status(500).send({message : "syntax err"});
    } finally{

    }
    

});


module.exports = router;
