
import jwt from "jsonwebtoken"
import dotenv from "dotenv"


/**
 * This function generates a JWT token for a user with the secret key set as an environment variable (JWT_SECRET_KEY)
 * @param user User object to generate token for
 * @returns JWT token
 */
export function generateToken(user) {
    dotenv.config()
    if (
        typeof process.env.JWT_SECRET_KEY === undefined ||
        process.env.JWT_SECRET_KEY === undefined
    ) {
        throw new Error("JWT_SECRET_KEY is not defined")
    }
    const token = jwt.sign(
        { _id: user._id?.toString(), name: user.userName },
        process.env.JWT_SECRET_KEY,
        {
            expiresIn: "3000 days",
        }
    )
    return token
}

/**
 * This function verifies a JWT token with the secret key set as an environment variable (JWT_SECRET_KEY)
 * @param token Token to verify
 * @returns Decoded token payload if valid, otherwise throws an error
 */
export function verifyToken(token) {
    dotenv.config()
    if (
        typeof process.env.JWT_SECRET_KEY === undefined ||
        process.env.JWT_SECRET_KEY === undefined
    ) {
        throw new Error("JWT_SECRET_KEY is not defined")
    }
    return jwt.verify(token, process.env.JWT_SECRET_KEY)
}
