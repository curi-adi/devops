import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { getPlayerName, setPlayerName, validatePlayerName } from '../utils/player';

function navLinkClass(isActive) {
  return [
    'rounded-md px-2 py-1 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/60',
    isActive ? 'text-white bg-white/10 font-medium' : 'text-gray-300 hover:text-white',
  ].join(' ');
}

function Navbar() {
  const location = useLocation();
  const [playerName, setPlayerNameState] = useState(getPlayerName());
  const [editing, setEditing] = useState(false);
  const [editValue, setEditValue] = useState(playerName);
  const [editError, setEditError] = useState(null);

  const savePlayerName = () => {
    const validationError = validatePlayerName(editValue);
    if (validationError) {
      setEditError(validationError);
      return;
    }
    const saved = setPlayerName(editValue);
    setPlayerNameState(saved);
    setEditing(false);
    setEditError(null);
  };

  const isHome = location.pathname === '/';
  const isLeaderboard = location.pathname === '/leaderboard';
  const isWiki = location.pathname.startsWith('/wiki');
  const isManage = location.pathname === '/manage-questions';

  return (
    <nav className="sticky top-0 z-40 bg-gray-900 text-white shadow-md">
      <div className="container mx-auto px-4 py-4">
        <div className="flex flex-wrap justify-between items-center gap-4">
          <Link
            to="/"
            className="text-xl font-bold tracking-tight hover:text-gray-200 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/60 rounded-md"
          >
            DevOps Dojo
          </Link>

          <div className="flex flex-wrap items-center gap-2 md:gap-4">
            <Link to="/" className={navLinkClass(isHome)}>
              Home
            </Link>
            <Link to="/leaderboard" className={navLinkClass(isLeaderboard)}>
              Leaderboard
            </Link>
            <Link to="/wiki" className={navLinkClass(isWiki)}>
              Wiki
            </Link>
            <Link to="/manage-questions" className={navLinkClass(isManage)}>
              Manage
            </Link>

            {editing ? (
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={editValue}
                  onChange={(e) => {
                    setEditValue(e.target.value);
                    setEditError(null);
                  }}
                  className="text-gray-900 px-2 py-1 rounded text-sm w-36 focus:outline-none focus:ring-2 focus:ring-blue-400"
                  placeholder="Your name"
                />
                <button
                  onClick={savePlayerName}
                  className="text-xs bg-blue-600 px-2 py-1 rounded hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-400"
                >
                  Save
                </button>
                <button
                  onClick={() => {
                    setEditing(false);
                    setEditError(null);
                  }}
                  className="text-xs text-gray-400 hover:text-white"
                >
                  Cancel
                </button>
                {editError && <span className="text-red-400 text-xs">{editError}</span>}
              </div>
            ) : (
              <button
                onClick={() => {
                  setEditValue(playerName);
                  setEditing(true);
                }}
                className="text-sm bg-gray-800 px-3 py-1 rounded-full hover:bg-gray-700 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/60"
                title="Click to change your leaderboard name"
              >
                {playerName || 'Set name'}
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
