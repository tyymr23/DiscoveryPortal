import React, { useState } from 'react'

const RunButton = () => {
    const [projectUrl, setProjectUrl] = useState("")
    const [loading, setLoading] = useState(false)

    const handleClick = async () => {
        setLoading(true)
        // we will replace this with API call later
        await new Promise((resolve) => setTimeout(resolve, 3000))
        const url = "https://www.google.com/"
        setProjectUrl(url)
        setLoading(false)
    }

    return (
        <div className='flex flex-row items-center gap-4 pt-4'>
            <button
                className={`w-40 py-2 rounded-lg transition duration-300 ${
                    loading || projectUrl
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-orange-400 text-white hover:bg-orange-500"
                }`}
                onClick={handleClick}
                disabled={loading || projectUrl}
            >
                {loading ? "Loading..." : "Run"}
            </button>

            {projectUrl && (
                <p className='text-lg'>
                    Project URL:{" "}
                    <a
                        href={projectUrl}
                        target='_blank'
                        rel='noopener noreferrer'
                        className='text-orange-400 font-semibold hover:underline'
                    >
                        {projectUrl}
                    </a>
                </p>
            )}
        </div>
    )

}

export default RunButton;