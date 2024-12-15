import { useRef, useEffect } from "react"
import io, { type Socket } from "socket.io-client"

function useSocketIO(url?: string) {
  const socketRef = useRef<Socket | null>(null);
  
  function connect() {
    socketRef.current = io(url)
  }

  function emitEvent(event: string, ...payload: unknown[]) {
    if (socketRef.current) {
      socketRef.current?.emit(event, ...payload)
    }
    else {
      throw new Error("emitEvent: socket ref is null")
    }
  }

  useEffect(connect, [url])

  return {
    emitEvent,
    isConnected: socketRef.current?.connected
  }
}

export default useSocketIO
