import React, { useEffect, useState } from 'react'

const RunButton = ({ runData, imageSubmitted, buildStatus, userRole }) => {
    const [projectUrl, setProjectUrl] = useState("")
    const [loading, setLoading] = useState(false)
    const [stopping, setStopping] = useState(false)

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
                await new Promise (resolve => setTimeout(resolve, 2000));
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

    const handleStop = async () => {
        setStopping(true)
        try {
            const res = await fetch(
                `${process.env.REACT_APP_API_BASE_URL}/projects/${runData.projectName}/stop`,
                { method: 'POST' }
            )
            const data = await res.json();
            if (data.is_stopped) {
                setProjectUrl("") // clear URL and show run again
            } else {
                console.error("Failed to stop container:", data)
            }
        } catch (err) {
            console.error("Error stopping the project:", err)
        } finally {
            setStopping(false)
        }
    }

    return (
        <div className='flex flex-row items-center gap-4 pt-4'>
            <button
                className={`w-40 py-2 rounded-lg transition duration-300 ${
                    buildStatus = "PENDING" || loading || projectUrl || !canRun
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-orange-400 text-white hover:bg-orange-500"
                }`}
                onClick={handleClick}
                disabled={loading || projectUrl || !canRun}
            >
                {buildStatus === "PENDING" ? "Building..." : loading ? "Loading..." : "Run Project"}
            </button>
            
            {!projectUrl && (
                <button className={`w-40 py-2 rounded-lg transition duration-300 ${
                    buildStatus === "PENDING" || loading || !canRun
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-orange-400 text-white hover:bg-orange-500"
                    }`}
                    onClick={handleClick}
                    disabled={buildStatus === "PENDING" || loading || !canRun}
                >
                    {buildStatus === "PENDING" ? "Building..." : loading ? "Loading..." : "Run Project"}
                </button>
            )}

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

            {projectUrl && userRole === "admin" && (
                <button className={`py-2 px-4 rounded-lg transition duration-300 ${
                    stopping
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-red-500 text-white hover:bg-red-600"
                    }`}
                    onClick={handleStop}
                    disabled={stopping}
                >
                    {stopping ? "Stopping..." : "Stop"}
                </button>
            )}
        </div>
    )
}

export default RunButton;