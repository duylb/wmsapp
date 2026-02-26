import { useEffect, useRef } from "react"

export const useRosterSocket = (
  companyId: string,
  onMessage: (data: any) => void
) => {
  const socketRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const socket = new WebSocket(
      `ws://localhost:8000/ws/roster/${companyId}`
    )

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      onMessage(data)
    }

    socketRef.current = socket

    return () => {
      socket.close()
    }
  }, [companyId])

  const send = (data: any) => {
    socketRef.current?.send(JSON.stringify(data))
  }

  return { send }
}