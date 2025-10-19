from enum import Enum
from typing import Dict


class ScraperStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"


class ScraperState:
    
    def __init__(self, maxPages: int):
        self.maxPages = maxPages
        self.status = ScraperStatus.IDLE
        self.currentPage = 0,
        self.totalBooksAdded = 0
        self.startTime = None
        self.endTime = None
        
    def start(self):
        self.status = ScraperStatus.RUNNING
        from time import time
        self.startTime = time()
        
    def pause(self):
        if self.status == ScraperStatus.RUNNING:
            self.status = ScraperStatus.PAUSED
        
    def resume(self):
        if self.status == ScraperStatus.PAUSED:
            self.status = ScraperStatus.RUNNING
    
    def togglePauseResume(self):
        if self.status == ScraperStatus.RUNNING:
            self.pause()
            return "paused"
        elif self.status == ScraperStatus.PAUSED:
            self.resume()
            return "resumed"
        
    def stop(self):
        self.status = ScraperStatus.STOPPED
        from time import time
        self.endTime = time()
    
    def addBooks(self, count: int):
        self.totalBooksAdded += count
        
    def setCurrentPage(self, page: int):
        self.currentPage = page
    
    def getProgressPercent(self) -> float:
        if self.maxPages == 0:
            return 0
        return (self.currentPage / self.maxPages) * 100
    def setCompleted(self):
        self.status = ScraperStatus.COMPLETED
        return
    def getStatus(self) -> Dict:
        return {
            'status': self.status.value,
            'currentPage': self.currentPage,
            'maxPages': self.maxPages,
            'progressPercent': self.getProgressPercent(),
            'totalBooksAdded': self.totalBooksAdded,
            'isPaused': self.status == ScraperStatus.PAUSED,
            'isRunning': self.status == ScraperStatus.RUNNING
        }

