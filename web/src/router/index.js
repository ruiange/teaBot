import express from "express";


const mainRouter  = express.Router();

mainRouter.post('/', async (req, res) => {
    console.log('post')


    const body = req.body;

    res.send({
        message: 'Hello World',
        code:200
    })
})
mainRouter.get('/', async (req, res) => {
    console.log('get')
    res.send({
        message: 'Hello World'
    })
})
export default mainRouter;