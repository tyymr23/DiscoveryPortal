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

    const normalize = raw => raw.startsWith('http://') || raw.startsWith('https://') ? raw : `http://${raw}`

    useEffect(() => {
        let timer
        const checkRunning = async () => {
          try {
            const res = await fetch(
              `${process.env.REACT_APP_API_BASE_URL}/projects/${runData.projectName}/running`
            )
            const body = await res.json()
            if (body.containerRunning && body.url) {
              const rawUrl = normalize(body.url)
              let finalUrl = rawUrl
              if (isAdmin && loading) {
                try {
                  finalUrl = await waitForApp(rawUrl)
                } catch (err) {
                  console.error("App readiness timed out, showing URL anyway:", err)
                }
              }
              setProjectUrl(finalUrl)
              setIsRunning(true)
              setLoading(false)
              clearInterval(timer)
            }
          } catch (err) {
            console.error("Error checking running container:", err)
          }
        }
    
        checkRunning()
        timer = setInterval(checkRunning, 2000)
        return () => clearInterval(timer)
      }, [runData.projectName, loading, isAdmin])

      const waitForApp = async (url) => {
        const maxAttempts = 10
        for (let attempt = 0; attempt < maxAttempts; attempt++) {
          try {
            const res = await fetch(url, { method: 'GET' })
            if (res.ok) return url
          } catch {
            // ignore network errors
          }
          await new Promise((r) => setTimeout(r, 1000))
        }
        throw new Error('App did not become ready in time')
      }

    const canRun = isBuilt || isRunning
    const disabled = isBuilding || loading || !canRun || !!projectUrl

    let buttonText = "Run"
    if (isBuilding) buttonText = "Building..."
    else if (loading) buttonText = "Starting..."

    const handleClick = async () => {
        setLoading(true);
        try {
            await fetch(
                `${process.env.REACT_APP_API_BASE_URL}/projects/${runData.projectName}/run`,
                { method: 'GET' }
            );
        } catch (error) {
            console.error("Error running the project:", error);
            setLoading(false)
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
            {isAdmin && (<button
                className={`w-32 py-2 rounded-lg transition duration-300 ${
                    disabled ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-orange-400 text-white hover:bg-orange-500'
                }`}
                onClick={handleClick}
                disabled={disabled}
            >
                {buttonText}
            </button>)}

            {!isAdmin && !projectUrl && (
                <p className='text-gray-500 italic'>
                    Container isn't currently running right now. Please request for an admin to build/start it when ready.
                </p>
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