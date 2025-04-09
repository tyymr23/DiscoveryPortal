import React, { useEffect, useState } from 'react'

const RunButton = ({ runData, imageSubmitted }) => {
    const [projectUrl, setProjectUrl] = useState("")
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        console.log("RunData recieved in RunButton:", runData);
    }, [runData])

    const canRun = imageSubmitted; // lets us know if we are ready to run image

    const handleClick = async () => {
        setLoading(true);
        try {
            const response = await fetch(
                `${process.env.REACT_APP_API_BASE_URL}/projects/${runData.projectName}/run`,
                { method: 'GET' }
            );
            const data = await response.json();
            if (data.url) {
                setProjectUrl(data.url);
            } else {
                console.error("No URL returned from API:", data);
            }
        } catch (error) {
            console.error("Error running the project:", error);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className='flex flex-row items-center gap-4 pt-4'>
            <button
                className={`w-40 py-2 rounded-lg transition duration-300 ${
                    loading || projectUrl || !canRun
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-orange-400 text-white hover:bg-orange-500"
                }`}
                onClick={handleClick}
                disabled={loading || projectUrl || !canRun}
            >
                {loading ? "Loading..." : "Run Project"}
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