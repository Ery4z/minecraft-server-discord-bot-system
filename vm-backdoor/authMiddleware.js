import { verifyToken } from "./jwt.js"
import dotenv from "dotenv"
//TODO: Create test for this function
dotenv.config()

/**
 * Middleware used to authenticate a user
 * @param req
 * @param res
 * @param next
 * @returns
 */
function Authenticate(req, res, next) {
    //! This is a temporary bypass for testing purposes
    //! Remove this when you are ready to implement authentication
    if (process.env.DEBUG_BYPASS_AUTH === "true") {
        next()
        return
    }

    if (req.headers.authorization === undefined) {
        res.status(401).send("Unauthorized")
        return
    }

    const token = req.headers.authorization.split(" ")[1]
    if (!token) {
        res.status(401).send("Unauthorized")
        return
    }

    try {
        const tokenPayload = verifyToken(token) 
        //
        if (tokenPayload.exp < Date.now() / 1000) {
            res.status(401).send("Unauthorized")
            return
        }
        if (!verifyToken(token)) {
            res.status(401).send("Unauthorized")
            return
        }
    } catch (error) {
        res.status(401).send("Unauthorized")
        return
    }
    next()
}


export { Authenticate }
