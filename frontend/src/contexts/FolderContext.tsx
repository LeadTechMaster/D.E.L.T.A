import { createContext, useContext, useState, type ReactNode } from "react";

export interface SavedItem {
  id: string;
  name: string;
  description: string;
  type: "map" | "dashboard" | "area";
  timestamp: Date;
  visible?: boolean;
  color?: string;
  // Area-specific data
  areaData?: {
    type: "zip" | "polygon" | "tract";
    zipcodes?: string[]; // For ZIP selection
    polygon?: [number, number][]; // For polygon drawing (lat/lng)
    tracts?: Array<{ // For tract-weighted demographics
      geoid: string;
      overlap_percentage: number;
    }>;
    demographics?: any; // Cached demographics data
    bounds?: { // Map bounds for zoom-to-fit
      north: number;
      south: number;
      east: number;
      west: number;
    };
  };
}

export interface Folder {
  id: string;
  name: string;
  description: string;
  items: SavedItem[];
  color: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  color: string;
  folders: Folder[];
  createdAt: Date;
}

interface FolderContextType {
  projects: Project[];
  addProject: (project: Omit<Project, "id" | "createdAt">) => void;
  updateProject: (id: string, updates: Partial<Project>) => void;
  deleteProject: (id: string) => void;
  addFolderToProject: (projectId: string, folder: Omit<Folder, "id">) => void;
  updateFolder: (
    projectIdOrFolderId: string, 
    folderIdOrUpdates: string | Partial<Folder>, 
    updates?: Partial<Folder>
  ) => void;
  deleteFolder: (projectIdOrFolderId: string, folderId?: string) => void;
  addItemToFolder: (
    projectIdOrFolderId: string, 
    folderIdOrItem: string | Omit<SavedItem, "id" | "timestamp">, 
    item?: Omit<SavedItem, "id" | "timestamp">
  ) => void;
  removeItemFromFolder: (
    projectIdOrFolderId: string, 
    folderIdOrItemId: string, 
    itemId?: string
  ) => void;
  updateItemInFolder: (
    projectIdOrFolderId: string, 
    folderIdOrItemId: string, 
    itemIdOrUpdates: string | Partial<SavedItem>, 
    updates?: Partial<SavedItem>
  ) => void;
  toggleItemVisibility: (projectId: string, folderId: string, itemId: string) => void;
  saveCurrentView: (name: string, description: string, type: "map" | "dashboard") => void;
  // Legacy compatibility - flatten all folders from all projects
  folders: Folder[];
  toggleFolderVisibility: (folderId: string) => void;
  moveFolderUp: (folderId: string) => void;
  moveFolderDown: (folderId: string) => void;
  // Drag and drop reordering
  reorderFolders: (dragIndex: number, hoverIndex: number) => void;
  moveAreaBetweenFolders: (dragFolderId: string, dragAreaId: string, hoverFolderId: string, hoverIndex: number) => void;
}

// Available colors palette
export const PROJECT_COLORS = [
  "#00bcd4", "#26c6da", "#4dd0e1", "#80deea", 
  "#b2ebf2", "#00acc1", "#0097a7", "#00838f"
];

// Legacy export for backward compatibility
export const FOLDER_COLORS = [
  "#fbbf24", // Yellow
  "#22c55e", // Green
  "#ef4444", // Red
  "#3b82f6", // Blue
];

const FolderContext = createContext<FolderContextType | undefined>(undefined);

// Sample placeholder data
const initialProjects: Project[] = [
  {
    id: "project-1",
    name: "Market Research 2024",
    description: "Comprehensive market analysis for Q4 2024",
    color: "#00bcd4",
    createdAt: new Date(2024, 9, 1),
    folders: [
      {
        id: "folder-1",
        name: "Downtown Analysis",
        description: "Market research for downtown district",
        color: "#00bcd4",
        items: [
          {
            id: "item-1",
            name: "Population Heatmap",
            description: "Downtown population density visualization",
            type: "map",
            timestamp: new Date(2024, 9, 5),
            visible: true,
            color: "#ef4444",
          },
          {
            id: "item-2",
            name: "Demographics Overview",
            description: "Key demographic indicators for downtown area",
            type: "dashboard",
            timestamp: new Date(2024, 9, 6),
            visible: true,
            color: "#ef4444",
          },
        ],
      },
      {
        id: "folder-2",
        name: "Suburban Expansion",
        description: "Growth opportunities in suburban areas",
        color: "#4dd0e1",
        items: [
          {
            id: "item-3",
            name: "Growth Trends",
            description: "5-year population and economic growth analysis",
            type: "dashboard",
            timestamp: new Date(2024, 9, 8),
            visible: true,
            color: "#22c55e",
          },
          {
            id: "item-4",
            name: "Housing Development",
            description: "New construction and housing market",
            type: "map",
            timestamp: new Date(2024, 9, 9),
            visible: true,
            color: "#fbbf24",
          },
        ],
      },
    ],
  },
  {
    id: "project-2",
    name: "Competitive Intelligence",
    description: "Competitor analysis and market positioning",
    color: "#0097a7",
    createdAt: new Date(2024, 8, 15),
    folders: [
      {
        id: "folder-3",
        name: "Location Analysis",
        description: "Competitor location mapping",
        color: "#0097a7",
        items: [
          {
            id: "item-5",
            name: "POI Clusters",
            description: "Competitor location mapping",
            type: "map",
            timestamp: new Date(2024, 9, 10),
            visible: true,
            color: "#3b82f6",
          },
        ],
      },
    ],
  },
];

export function FolderProvider({ children }: { children: ReactNode }) {
  const [projects, setProjects] = useState<Project[]>(initialProjects);

  const addProject = (project: Omit<Project, "id" | "createdAt">) => {
    const newProject: Project = {
      ...project,
      id: `project-${Date.now()}`,
      createdAt: new Date(),
    };
    setProjects([...projects, newProject]);
  };

  const updateProject = (id: string, updates: Partial<Project>) => {
    setProjects(projects.map(p => p.id === id ? { ...p, ...updates } : p));
  };

  const deleteProject = (id: string) => {
    setProjects(projects.filter(p => p.id !== id));
  };

  const addFolderToProject = (projectId: string, folder: Omit<Folder, "id">) => {
    const newFolder: Folder = {
      ...folder,
      id: `folder-${Date.now()}`,
      items: folder.items || [], // Ensure items array exists
    };
    setProjects(projects.map(p =>
      p.id === projectId
        ? { ...p, folders: [...(p.folders || []), newFolder] }
        : p
    ));
  };

  // Overloaded updateFolder to support both old (folderId, updates) and new (projectId, folderId, updates) signatures
  const updateFolder = (
    projectIdOrFolderId: string, 
    folderIdOrUpdates: string | Partial<Folder>, 
    updates?: Partial<Folder>
  ) => {
    // New signature: updateFolder(projectId, folderId, updates)
    if (typeof folderIdOrUpdates === 'string' && updates) {
      const projectId = projectIdOrFolderId;
      const folderId = folderIdOrUpdates;
      setProjects(projects.map(p =>
        p.id === projectId
          ? {
              ...p,
              folders: (p.folders || []).map(f =>
                f?.id === folderId ? { ...f, ...updates, items: (f.items || []) } : f
              ),
            }
          : p
      ));
    } 
    // Old signature: updateFolder(folderId, updates) - for backward compatibility
    else if (typeof folderIdOrUpdates === 'object') {
      const folderId = projectIdOrFolderId;
      const folderUpdates = folderIdOrUpdates;
      setProjects(projects.map(p => ({
        ...p,
        folders: (p.folders || []).map(f =>
          f?.id === folderId ? { ...f, ...folderUpdates, items: (f.items || []) } : f
        ),
      })));
    }
  };

  // Overloaded deleteFolder to support both old (folderId) and new (projectId, folderId) signatures
  const deleteFolder = (projectIdOrFolderId: string, folderId?: string) => {
    if (folderId) {
      // New signature: deleteFolder(projectId, folderId)
      const projectId = projectIdOrFolderId;
      setProjects(projects.map(p =>
        p.id === projectId
          ? { ...p, folders: (p.folders || []).filter(f => f?.id !== folderId) }
          : p
      ));
    } else {
      // Old signature: deleteFolder(folderId) - for backward compatibility
      const folderIdToDelete = projectIdOrFolderId;
      setProjects(projects.map(p => ({
        ...p,
        folders: (p.folders || []).filter(f => f?.id !== folderIdToDelete),
      })));
    }
  };

  // Overloaded addItemToFolder to support both signatures
  const addItemToFolder = (
    projectIdOrFolderId: string, 
    folderIdOrItem: string | Omit<SavedItem, "id" | "timestamp">, 
    item?: Omit<SavedItem, "id" | "timestamp">
  ) => {
    const newItem: SavedItem = {
      ...(item || folderIdOrItem as Omit<SavedItem, "id" | "timestamp">),
      id: `item-${Date.now()}`,
      timestamp: new Date(),
      visible: true,
    };
    
    if (typeof folderIdOrItem === 'string' && item) {
      // New signature: addItemToFolder(projectId, folderId, item)
      const projectId = projectIdOrFolderId;
      const folderId = folderIdOrItem;
      setProjects(projects.map(p =>
        p.id === projectId
          ? {
              ...p,
              folders: (p.folders || []).map(f =>
                f?.id === folderId
                  ? { ...f, items: [...(f.items || []), newItem] }
                  : f
              ),
            }
          : p
      ));
    } else {
      // Old signature: addItemToFolder(folderId, item) - for backward compatibility
      const folderId = projectIdOrFolderId;
      setProjects(projects.map(p => ({
        ...p,
        folders: (p.folders || []).map(f =>
          f?.id === folderId
            ? { ...f, items: [...(f.items || []), newItem] }
            : f
        ),
      })));
    }
  };

  // Overloaded removeItemFromFolder to support both signatures
  const removeItemFromFolder = (
    projectIdOrFolderId: string, 
    folderIdOrItemId: string, 
    itemId?: string
  ) => {
    if (itemId) {
      // New signature: removeItemFromFolder(projectId, folderId, itemId)
      const projectId = projectIdOrFolderId;
      const folderId = folderIdOrItemId;
      setProjects(projects.map(p =>
        p.id === projectId
          ? {
              ...p,
              folders: (p.folders || []).map(f =>
                f?.id === folderId
                  ? { ...f, items: (f.items || []).filter(item => item?.id !== itemId) }
                  : f
              ),
            }
          : p
      ));
    } else {
      // Old signature: removeItemFromFolder(folderId, itemId) - for backward compatibility
      const folderId = projectIdOrFolderId;
      const itemIdToRemove = folderIdOrItemId;
      setProjects(projects.map(p => ({
        ...p,
        folders: (p.folders || []).map(f =>
          f?.id === folderId
            ? { ...f, items: (f.items || []).filter(item => item?.id !== itemIdToRemove) }
            : f
        ),
      })));
    }
  };

  // Overloaded updateItemInFolder to support both signatures
  const updateItemInFolder = (
    projectIdOrFolderId: string, 
    folderIdOrItemId: string, 
    itemIdOrUpdates: string | Partial<SavedItem>, 
    updates?: Partial<SavedItem>
  ) => {
    if (typeof itemIdOrUpdates === 'string' && updates) {
      // New signature: updateItemInFolder(projectId, folderId, itemId, updates)
      const projectId = projectIdOrFolderId;
      const folderId = folderIdOrItemId;
      const itemId = itemIdOrUpdates;
      setProjects(projects.map(p =>
        p.id === projectId
          ? {
              ...p,
              folders: (p.folders || []).map(f =>
                f?.id === folderId
                  ? {
                      ...f,
                      items: (f.items || []).map(item =>
                        item?.id === itemId ? { ...item, ...updates } : item
                      ),
                    }
                  : f
              ),
            }
          : p
      ));
    } else if (typeof itemIdOrUpdates === 'object') {
      // Old signature: updateItemInFolder(folderId, itemId, updates) - for backward compatibility
      const folderId = projectIdOrFolderId;
      const itemId = folderIdOrItemId;
      const itemUpdates = itemIdOrUpdates;
      setProjects(projects.map(p => ({
        ...p,
        folders: (p.folders || []).map(f =>
          f?.id === folderId
            ? {
                ...f,
                items: (f.items || []).map(item =>
                  item?.id === itemId ? { ...item, ...itemUpdates } : item
                ),
              }
            : f
        ),
      })));
    }
  };

  const toggleItemVisibility = (projectId: string, folderId: string, itemId: string) => {
    setProjects(projects.map(p =>
      p.id === projectId
        ? {
            ...p,
            folders: (p.folders || []).map(f =>
              f?.id === folderId
                ? {
                    ...f,
                    items: (f.items || []).map(item =>
                      item?.id === itemId
                        ? { ...item, visible: !item.visible }
                        : item
                    ),
                  }
                : f
            ),
          }
        : p
    ));
  };

  const saveCurrentView = (name: string, description: string, type: "map" | "dashboard") => {
    // Save to the latest folder (most recently created) in the first project
    if (projects.length > 0 && projects[0].folders.length > 0) {
      // Get the latest folder (last in the array)
      const latestFolder = projects[0].folders[projects[0].folders.length - 1];
      addItemToFolder(projects[0].id, latestFolder.id, { name, description, type });
    } else if (projects.length > 0) {
      // Add folder to first project
      addFolderToProject(projects[0].id, {
        name: "General",
        description: "General saved views",
        color: "#00bcd4",
        items: [],
      });
      // After adding the folder, we need to save the item to it
      // The folder will be the last one in the array
      setTimeout(() => {
        const updatedProject = projects.find(p => p.id === projects[0].id);
        if (updatedProject && updatedProject.folders.length > 0) {
          const latestFolder = updatedProject.folders[updatedProject.folders.length - 1];
          addItemToFolder(projects[0].id, latestFolder.id, { name, description, type });
        }
      }, 0);
    } else {
      // Create new project
      const newProject: Omit<Project, "id" | "createdAt"> = {
        name: "My Project",
        description: "Saved views and analyses",
        color: "#00bcd4",
        folders: [
          {
            id: `folder-${Date.now()}`,
            name: "General",
            description: "General saved views",
            color: "#00bcd4",
            items: [],
          },
        ],
      };
      addProject(newProject);
    }
  };

  // Legacy compatibility: flatten all folders from all projects
  const folders = projects.flatMap(project => 
    project.folders.map(folder => ({
      ...folder,
      createdAt: project.createdAt,
      visible: true,
    }))
  );

  const toggleFolderVisibility = (folderId: string) => {
    // Find which project contains this folder
    for (const project of projects) {
      const folder = project.folders.find(f => f.id === folderId);
      if (folder) {
        // For legacy compatibility, we'll just log this
        console.log('Toggle folder visibility:', folderId);
        break;
      }
    }
  };

  const moveFolderUp = (folderId: string) => {
    // For legacy compatibility, we'll implement this within a project
    for (const project of projects) {
      if (!project?.folders) continue;
      const folderIndex = project.folders.findIndex(f => f?.id === folderId);
      if (folderIndex > 0) {
        const newFolders = [...project.folders];
        [newFolders[folderIndex - 1], newFolders[folderIndex]] = 
          [newFolders[folderIndex], newFolders[folderIndex - 1]];
        updateProject(project.id, { folders: newFolders });
        break;
      }
    }
  };

  const moveFolderDown = (folderId: string) => {
    // For legacy compatibility, we'll implement this within a project
    for (const project of projects) {
      if (!project?.folders) continue;
      const folderIndex = project.folders.findIndex(f => f?.id === folderId);
      if (folderIndex !== -1 && folderIndex < project.folders.length - 1) {
        const newFolders = [...project.folders];
        [newFolders[folderIndex], newFolders[folderIndex + 1]] = 
          [newFolders[folderIndex + 1], newFolders[folderIndex]];
        updateProject(project.id, { folders: newFolders });
        break;
      }
    }
  };

  const reorderFolders = (dragIndex: number, hoverIndex: number) => {
    // Reorder folders within the first project (for backward compatibility)
    if (projects.length > 0 && projects[0]?.folders) {
      const project = projects[0];
      const newFolders = [...(project.folders || [])];
      
      // Validate indices
      if (dragIndex >= 0 && dragIndex < newFolders.length && 
          hoverIndex >= 0 && hoverIndex <= newFolders.length) {
        const [draggedFolder] = newFolders.splice(dragIndex, 1);
        if (draggedFolder) {
          newFolders.splice(hoverIndex, 0, draggedFolder);
          updateProject(project.id, { folders: newFolders });
        }
      }
    }
  };

  const moveAreaBetweenFolders = (
    dragFolderId: string,
    dragAreaId: string,
    hoverFolderId: string,
    hoverIndex: number
  ) => {
    // Find the project containing the folders
    for (const project of projects) {
      if (!project?.folders) continue;
      
      const dragFolder = project.folders.find(f => f?.id === dragFolderId);
      const hoverFolder = project.folders.find(f => f?.id === hoverFolderId);
      
      if (dragFolder && hoverFolder) {
        const draggedItem = (dragFolder.items || []).find(item => item?.id === dragAreaId);
        
        if (draggedItem) {
          // Remove item from source folder
          const newDragFolderItems = (dragFolder.items || []).filter(item => item?.id !== dragAreaId);
          
          // Add item to target folder at specific index
          const newHoverFolderItems = [...(hoverFolder.items || [])];
          newHoverFolderItems.splice(hoverIndex, 0, draggedItem);
          
          // Update both folders
          const newFolders = project.folders.map(f => {
            if (!f) return f;
            if (f.id === dragFolderId) {
              return { ...f, items: newDragFolderItems };
            } else if (f.id === hoverFolderId) {
              return { ...f, items: newHoverFolderItems };
            }
            return f;
          });
          
          updateProject(project.id, { folders: newFolders });
          break;
        }
      }
    }
  };

  return (
    <FolderContext.Provider
      value={{
        projects,
        addProject,
        updateProject,
        deleteProject,
        addFolderToProject,
        updateFolder,
        deleteFolder,
        addItemToFolder,
        removeItemFromFolder,
        updateItemInFolder,
        toggleItemVisibility,
        saveCurrentView,
        // Legacy compatibility
        folders,
        toggleFolderVisibility,
        moveFolderUp,
        moveFolderDown,
        // Drag and drop
        reorderFolders,
        moveAreaBetweenFolders,
      }}
    >
      {children}
    </FolderContext.Provider>
  );
}

export function useFolders() {
  const context = useContext(FolderContext);
  if (context === undefined) {
    throw new Error("useFolders must be used within a FolderProvider");
  }
  return context;
}

