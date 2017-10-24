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
        var option = {
            mode: 'text',
            pythonPath: '',
            pythonOptions: ['-u'],
            scriptPath: '',
            args: [req.file.path]
        };
        python.run('./pylib/pitch.py', option, function (err, result) {
            if (err) {
                console.log('Something Gone Wrong!', err);
            }
            console.log('result is : ', result);
            res.status(200).send({ result: "success" });
        });
    } catch (err) {
        console.log('err msg: ', err);
        res.status(500).send({ message: "syntax err" });
    } finally {

    }


});


router.all('/test', (req, res)=>{
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
            res.status(200).send({ result: result });
        });
    } catch(err){
        console.log('err msg: ', err);
        res.status(500).send({message : "syntax err"});
    } finally{

    }
    

});


module.exports = router;