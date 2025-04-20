import React, { useEffect, useState } from 'react'

const RunButton = ({ runData, buildStatus }) => {
    const [projectUrl, setProjectUrl] = useState("")
    const [loading, setLoading] = useState(false)
    const [stopLoading, setStopLoading] = useState(false)
    const [isRunning, setIsRunning] = useState(false)

    const userRole = localStorage.getItem('userRole')
    const isAdmin = userRole === "admin"

    const isBuilding = buildStatus === "PENDING"
    const isBuilt = buildStatus === "SUCCESS"

    useEffect(() => {
        const checkRunning = async() => {
            try {
                const response = await fetch(
                    `${process.env.REACT_APP_API_BASE_URL}/projects/${runData.projectName}/running`
                )
                const data = await response.json()
                if (data.containerRunning && data.url) {
                    setProjectUrl(data.url)
                    setIsRunning(true)
                }
            } catch (err) {
                console.err("Error checking running container:", err)
            }
        }
        checkRunning();
    }, [runData.projectName])

    const canRun = isBuilt || isRunning
    const disabled = isBuilding || loading || !canRun || !!projectUrl

    let buttonText = "Run"
    if (isBuilding) buttonText = "Building..."
    else if (loading) buttonText = "Starting..."

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
                setIsRunning(true);
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
        setStopLoading(true)
        try {
            const response = await fetch(
                `${process.env.REACT_APP_API_BASE_URL}/projects/${runData.projectName}/stop`,
                { method: 'POST' }
            );
            const data = await response.json()
            if (data.is_stopped) {
                setProjectUrl("")
                setIsRunning(false)
            } else {
                console.error("Failed to stop container:", data)
            }
        } catch (err) {
            console.error("Error stopping the project:", err)
        } finally {
            setStopLoading(false);
        }
    }

    return (
        <div className='flex flex-row items-center gap-4 pt-4'>
            <button
                className={`w-32 py-2 rounded-lg transition duration-300 ${
                    disabled ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-orange-400 text-white hover:bg-orange-500'
                }`}
                onClick={handleClick}
                disabled={disabled}
            >
                {buttonText}
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

            {projectUrl && isAdmin && (
                <button
                    className={`w-32 py-2 rounded-lg transition duration-300 ${
                        stopLoading
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-red-500 text-white hover:bg-red-600'
                    }`}
                    onClick={handleStop}
                    disabled={stopLoading}
                >
                    {stopLoading ? 'Stopping...' : 'Stop'}
                </button>
            )}
        </div>
    )
}

export default RunButton;