import { useRef, useEffect } from "react"
import io, { type Socket } from "socket.io-client"

function useSocketIO(url?: string) {
  const socketRef = useRef<Socket | null>(null);
  
  function connect() {
    socketRef.current = io(url)
  }

  function on(event: string, listener: (...args: unknown[]) => void) {
    if (socketRef.current) {
      socketRef.current?.on(event, listener)
    }
    else {
      throw new Error("on: socket ref is null")
    }
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
    on,
    emitEvent,
    isConnected: socketRef.current?.connected
  }
}

export default useSocketIO
