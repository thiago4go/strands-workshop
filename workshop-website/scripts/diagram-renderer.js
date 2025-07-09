/**
 * Diagram Renderer for AWS Strands Workshop
 * Converts text-based diagrams to interactive visual representations
 */

class DiagramRenderer {
    constructor() {
        this.mermaidInitialized = false;
        this.init();
    }

    async init() {
        // Load Mermaid.js if not already loaded
        if (typeof mermaid === 'undefined') {
            await this.loadMermaid();
        }
        
        // Configure Mermaid
        mermaid.initialize({
            startOnLoad: false,
            theme: 'default',
            themeVariables: {
                primaryColor: '#007bff',
                primaryTextColor: '#333',
                primaryBorderColor: '#007bff',
                lineColor: '#666',
                secondaryColor: '#f8f9fa',
                tertiaryColor: '#e9ecef',
                background: '#ffffff',
                mainBkg: '#ffffff',
                secondBkg: '#f8f9fa',
                tertiaryBkg: '#e9ecef'
            },
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            },
            sequence: {
                diagramMarginX: 50,
                diagramMarginY: 10,
                actorMargin: 50,
                width: 150,
                height: 65,
                boxMargin: 10,
                boxTextMargin: 5,
                noteMargin: 10,
                messageMargin: 35,
                mirrorActors: true,
                bottomMarginAdj: 1,
                useMaxWidth: true
            }
        });

        this.mermaidInitialized = true;
        this.renderAllDiagrams();
    }

    async loadMermaid() {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    async renderAllDiagrams() {
        if (!this.mermaidInitialized) {
            console.warn('Mermaid not initialized yet');
            return;
        }

        // Find all text-based diagrams and convert them
        const diagramContainers = document.querySelectorAll('.mermaid-diagram, .architecture-diagram .diagram-container');
        
        for (let i = 0; i < diagramContainers.length; i++) {
            const container = diagramContainers[i];
            await this.renderDiagram(container, i);
        }

        // Add interactive features
        this.addInteractiveFeatures();
    }

    async renderDiagram(container, index) {
        try {
            // Get the text content
            const textContent = container.textContent || container.innerText;
            
            // Skip if already rendered
            if (container.querySelector('.mermaid-rendered')) {
                return;
            }

            // Create diagram based on content
            let mermaidCode = '';
            
            if (textContent.includes('Tool Integration Architecture')) {
                mermaidCode = this.createModule2Architecture();
            } else if (textContent.includes('Multi-Agent Research Team Architecture')) {
                mermaidCode = this.createModule3Architecture();
            } else if (textContent.includes('graph TB') || textContent.includes('graph TD')) {
                // Extract existing mermaid code
                mermaidCode = this.extractMermaidCode(textContent);
            } else {
                // Create a generic flowchart
                mermaidCode = this.createGenericFlowchart(textContent);
            }

            if (mermaidCode) {
                // Create container for rendered diagram
                const diagramDiv = document.createElement('div');
                diagramDiv.className = 'mermaid-rendered';
                diagramDiv.id = `diagram-${index}`;
                
                // Render the diagram
                const { svg } = await mermaid.render(`diagram-svg-${index}`, mermaidCode);
                diagramDiv.innerHTML = svg;
                
                // Add controls
                const controlsDiv = this.createDiagramControls(index);
                
                // Replace or append to container
                container.innerHTML = '';
                container.appendChild(controlsDiv);
                container.appendChild(diagramDiv);
                
                // Add styling
                container.classList.add('interactive-diagram');
                
                // Initialize pan and zoom functionality
                this.initializePanZoom(diagramDiv, index);
            }
        } catch (error) {
            console.error('Error rendering diagram:', error);
            // Fallback to original text
            container.innerHTML = `<div class="diagram-error">Diagram rendering failed. <button onclick="location.reload()">Retry</button></div>`;
        }
    }

    createModule2Architecture() {
        return `
graph TB
    User[👤 User Input] --> Agent[🤖 Enhanced Agent]
    Agent --> BuiltinTools[📦 Built-in Tools<br/>calculator, current_time]
    Agent --> CustomTools[🛠️ Custom Tools<br/>@tool decorated functions]
    Agent --> MCPTools[🌐 MCP Tools<br/>External integrations]
    
    BuiltinTools --> ToolExecution[⚙️ Tool Execution]
    CustomTools --> ToolExecution
    MCPTools --> ToolExecution
    
    MCPTools --> FilesystemServer[📁 Filesystem Server<br/>@modelcontextprotocol/server-filesystem]
    MCPTools --> MemoryServer[🧠 Memory Server<br/>@modelcontextprotocol/server-memory]
    
    FilesystemServer --> NodeJS1[🟢 Node.js Process]
    MemoryServer --> NodeJS2[🟢 Node.js Process]
    
    ToolExecution --> BedrockModel[🧠 Bedrock Model<br/>Claude 3.7 Sonnet]
    BedrockModel --> AWSBedrock[☁️ AWS Bedrock]
    AWSBedrock --> Response[📄 Enhanced Response]
    
    classDef userClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef agentClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef toolClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef mcpClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef awsClass fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    class User userClass
    class Agent agentClass
    class BuiltinTools,CustomTools,MCPTools toolClass
    class FilesystemServer,MemoryServer,NodeJS1,NodeJS2 mcpClass
    class BedrockModel,AWSBedrock,Response awsClass
        `;
    }

    createModule3Architecture() {
        return `
graph TB
    User[👤 User Research Request] --> ResearchTeam[🎯 ResearchTeam Class<br/>Agents-as-Tools Coordinator]
    ResearchTeam --> MCPSetup[🌐 MCP Client Setup<br/>DuckDuckGo + Sequential Thinking]
    
    MCPSetup --> ContextManager[🔄 Context Manager<br/>ExitStack with MCP Clients]
    ContextManager --> Orchestrator[🤖 Orchestrator Agent<br/>ResearchOrchestrator]
    
    Orchestrator --> SpecialistTools[🛠️ Specialist Agent Tools<br/>@tool wrapped agents]
    
    SpecialistTools --> ResearchTool[🔍 @tool research_specialist<br/>Web Research via DuckDuckGo]
    SpecialistTools --> AnalysisTool[📊 @tool analysis_specialist<br/>Sequential Thinking Analysis]
    SpecialistTools --> FactCheckTool[✅ @tool factcheck_specialist<br/>Fact Verification via DuckDuckGo]
    SpecialistTools --> QualityTool[🏆 @tool quality_specialist<br/>Quality Assessment]
    
    ResearchTool --> ResearchAgent[🔬 Research Agent<br/>ResearchSpecialist]
    AnalysisTool --> AnalysisAgent[📈 Analysis Agent<br/>AnalysisSpecialist]
    FactCheckTool --> FactCheckAgent[🔍 Fact-Check Agent<br/>FactCheckSpecialist]
    QualityTool --> QualityAgent[⭐ Quality Agent<br/>QualityAssuranceSpecialist]
    
    ResearchAgent --> DuckDuckGoTools[🌐 DuckDuckGo MCP Tools<br/>Web Search Capabilities]
    AnalysisAgent --> SequentialTools[🧠 Sequential Thinking Tools<br/>Structured Reasoning]
    FactCheckAgent --> DuckDuckGoTools
    QualityAgent --> CombinedTools[🔧 Combined Tools<br/>Sequential + DuckDuckGo]
    
    DuckDuckGoTools --> MCPDuckDuckGo[🐳 MCP DuckDuckGo Server<br/>Docker Container]
    SequentialTools --> MCPSequential[🐳 MCP Sequential Server<br/>Docker Container]
    CombinedTools --> MCPDuckDuckGo
    CombinedTools --> MCPSequential
    
    MCPDuckDuckGo --> WebSearchResults[🔍 Real Web Search Results]
    MCPSequential --> StructuredAnalysis[🧠 Structured Reasoning Output]
    
    WebSearchResults --> ResearchResult[📋 ResearchResult<br/>Comprehensive Report]
    StructuredAnalysis --> ResearchResult
    ResearchResult --> PerformanceMetrics[📊 Performance Metrics<br/>Quality Scores & Execution Time]
    
    classDef userClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef coordinatorClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef agentClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef toolClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef mcpClass fill:#ffebee,stroke:#c62828,stroke-width:2px
    classDef resultClass fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    
    class User userClass
    class ResearchTeam,MCPSetup,ContextManager,Orchestrator coordinatorClass
    class ResearchAgent,AnalysisAgent,FactCheckAgent,QualityAgent agentClass
    class SpecialistTools,ResearchTool,AnalysisTool,FactCheckTool,QualityTool toolClass
    class DuckDuckGoTools,SequentialTools,CombinedTools,MCPDuckDuckGo,MCPSequential mcpClass
    class WebSearchResults,StructuredAnalysis,ResearchResult,PerformanceMetrics resultClass
        `;
    }

    extractMermaidCode(textContent) {
        // Extract mermaid code from text content
        const lines = textContent.split('\n');
        const mermaidLines = [];
        let inMermaidBlock = false;
        
        for (const line of lines) {
            if (line.trim().startsWith('graph ') || line.trim().startsWith('sequenceDiagram') || line.trim().startsWith('flowchart')) {
                inMermaidBlock = true;
            }
            
            if (inMermaidBlock) {
                mermaidLines.push(line.trim());
            }
        }
        
        return mermaidLines.join('\n');
    }

    createGenericFlowchart(textContent) {
        // Create a simple flowchart from text content
        return `
graph TD
    A[Start] --> B[Process]
    B --> C[End]
        `;
    }

    createDiagramControls(index) {
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'diagram-controls';
        controlsDiv.innerHTML = `
            <div class="diagram-toolbar">
                <button class="btn-diagram-control" onclick="diagramRenderer.zoomIn(${index})" title="Zoom In">
                    🔍+
                </button>
                <button class="btn-diagram-control" onclick="diagramRenderer.zoomOut(${index})" title="Zoom Out">
                    🔍-
                </button>
                <button class="btn-diagram-control" onclick="diagramRenderer.resetView(${index})" title="Reset View">
                    ↻
                </button>
                <button class="btn-diagram-control" onclick="diagramRenderer.toggleFullscreen(${index})" title="Fullscreen">
                    ⛶
                </button>
            </div>
        `;
        return controlsDiv;
    }

    addInteractiveFeatures() {
        // Add CSS for interactive features
        const style = document.createElement('style');
        style.textContent = `
            .interactive-diagram {
                border: 1px solid #ddd;
                border-radius: 8px;
                margin: 20px 0;
                background: #fff;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .diagram-controls {
                background: #f8f9fa;
                border-bottom: 1px solid #ddd;
                padding: 10px;
                border-radius: 8px 8px 0 0;
            }
            
            .diagram-toolbar {
                display: flex;
                gap: 8px;
                align-items: center;
            }
            
            .btn-diagram-control {
                background: #007bff;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                transition: background-color 0.2s;
            }
            
            .btn-diagram-control:hover {
                background: #0056b3;
            }
            
            .mermaid-rendered {
                padding: 20px;
                text-align: center;
                overflow: auto;
                transition: transform 0.2s;
            }
            
            .mermaid-rendered svg {
                max-width: 100%;
                height: auto;
            }
            
            .diagram-fullscreen {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: white;
                z-index: 9999;
                display: flex;
                flex-direction: column;
            }
            
            .diagram-fullscreen .mermaid-rendered {
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .diagram-error {
                padding: 20px;
                text-align: center;
                color: #dc3545;
                background: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 4px;
                margin: 10px 0;
            }
        `;
        document.head.appendChild(style);
    }

    // Initialize pan and zoom for a diagram
    initializePanZoom(diagramElement, index) {
        let scale = 1;
        let translateX = 0;
        let translateY = 0;
        let isDragging = false;
        let startX = 0;
        let startY = 0;
        
        // Store state on the element
        diagramElement.panZoomState = {
            scale: 1,
            translateX: 0,
            translateY: 0
        };
        
        // Apply transform
        const applyTransform = () => {
            diagramElement.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
            diagramElement.style.transformOrigin = '0 0';
            diagramElement.panZoomState = { scale, translateX, translateY };
        };
        
        // Mouse wheel zoom
        diagramElement.addEventListener('wheel', (e) => {
            e.preventDefault();
            const rect = diagramElement.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            
            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            const newScale = Math.max(0.5, Math.min(3, scale * delta));
            
            if (newScale !== scale) {
                const scaleChange = newScale / scale;
                translateX = mouseX - (mouseX - translateX) * scaleChange;
                translateY = mouseY - (mouseY - translateY) * scaleChange;
                scale = newScale;
                applyTransform();
            }
        });
        
        // Mouse drag pan
        diagramElement.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX - translateX;
            startY = e.clientY - translateY;
            diagramElement.style.cursor = 'grabbing';
            e.preventDefault();
        });
        
        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                translateX = e.clientX - startX;
                translateY = e.clientY - startY;
                applyTransform();
            }
        });
        
        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                diagramElement.style.cursor = scale > 1 ? 'grab' : 'default';
            }
        });
        
        // Touch support for mobile
        let lastTouchDistance = 0;
        
        diagramElement.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
                isDragging = true;
                startX = e.touches[0].clientX - translateX;
                startY = e.touches[0].clientY - translateY;
            } else if (e.touches.length === 2) {
                const touch1 = e.touches[0];
                const touch2 = e.touches[1];
                lastTouchDistance = Math.sqrt(
                    Math.pow(touch2.clientX - touch1.clientX, 2) +
                    Math.pow(touch2.clientY - touch1.clientY, 2)
                );
            }
            e.preventDefault();
        });
        
        diagramElement.addEventListener('touchmove', (e) => {
            if (e.touches.length === 1 && isDragging) {
                translateX = e.touches[0].clientX - startX;
                translateY = e.touches[0].clientY - startY;
                applyTransform();
            } else if (e.touches.length === 2) {
                const touch1 = e.touches[0];
                const touch2 = e.touches[1];
                const currentDistance = Math.sqrt(
                    Math.pow(touch2.clientX - touch1.clientX, 2) +
                    Math.pow(touch2.clientY - touch1.clientY, 2)
                );
                
                if (lastTouchDistance > 0) {
                    const scaleChange = currentDistance / lastTouchDistance;
                    const newScale = Math.max(0.5, Math.min(3, scale * scaleChange));
                    
                    if (newScale !== scale) {
                        const centerX = (touch1.clientX + touch2.clientX) / 2;
                        const centerY = (touch1.clientY + touch2.clientY) / 2;
                        const rect = diagramElement.getBoundingClientRect();
                        const mouseX = centerX - rect.left;
                        const mouseY = centerY - rect.top;
                        
                        const actualScaleChange = newScale / scale;
                        translateX = mouseX - (mouseX - translateX) * actualScaleChange;
                        translateY = mouseY - (mouseY - translateY) * actualScaleChange;
                        scale = newScale;
                        applyTransform();
                    }
                }
                lastTouchDistance = currentDistance;
            }
            e.preventDefault();
        });
        
        diagramElement.addEventListener('touchend', () => {
            isDragging = false;
            lastTouchDistance = 0;
        });
        
        // Set initial cursor
        diagramElement.style.cursor = 'grab';
        
        // Store functions for external access
        diagramElement.zoomIn = () => {
            const newScale = Math.min(3, scale * 1.2);
            if (newScale !== scale) {
                const rect = diagramElement.getBoundingClientRect();
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const scaleChange = newScale / scale;
                translateX = centerX - (centerX - translateX) * scaleChange;
                translateY = centerY - (centerY - translateY) * scaleChange;
                scale = newScale;
                applyTransform();
                diagramElement.style.cursor = scale > 1 ? 'grab' : 'default';
            }
        };
        
        diagramElement.zoomOut = () => {
            const newScale = Math.max(0.5, scale * 0.8);
            if (newScale !== scale) {
                const rect = diagramElement.getBoundingClientRect();
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const scaleChange = newScale / scale;
                translateX = centerX - (centerX - translateX) * scaleChange;
                translateY = centerY - (centerY - translateY) * scaleChange;
                scale = newScale;
                applyTransform();
                diagramElement.style.cursor = scale > 1 ? 'grab' : 'default';
            }
        };
        
        diagramElement.resetView = () => {
            scale = 1;
            translateX = 0;
            translateY = 0;
            applyTransform();
            diagramElement.style.cursor = 'default';
        };
    }

    // Interactive control methods
    zoomIn(index) {
        const diagram = document.querySelector(`#diagram-${index}`);
        if (diagram && diagram.zoomIn) {
            diagram.zoomIn();
        }
    }

    zoomOut(index) {
        const diagram = document.querySelector(`#diagram-${index}`);
        if (diagram && diagram.zoomOut) {
            diagram.zoomOut();
        }
    }

    resetView(index) {
        const diagram = document.querySelector(`#diagram-${index}`);
        if (diagram && diagram.resetView) {
            diagram.resetView();
        }
    }

    toggleFullscreen(index) {
        const container = document.querySelector(`#diagram-${index}`).parentElement;
        if (container.classList.contains('diagram-fullscreen')) {
            container.classList.remove('diagram-fullscreen');
            document.body.style.overflow = '';
        } else {
            container.classList.add('diagram-fullscreen');
            document.body.style.overflow = 'hidden';
        }
    }
}

// Initialize diagram renderer when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.diagramRenderer = new DiagramRenderer();
});

// Also initialize if DOM is already loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        window.diagramRenderer = new DiagramRenderer();
    });
} else {
    window.diagramRenderer = new DiagramRenderer();
}
