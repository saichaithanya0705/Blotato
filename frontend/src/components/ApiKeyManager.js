import React, { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "./ui/dialog";
import { useToast } from "../hooks/use-toast";
import { Key, Plus, Trash2, Copy, Eye, EyeOff } from "lucide-react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ApiKeyManager = () => {
  const [apiKeys, setApiKeys] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [newKeyName, setNewKeyName] = useState("");
  const [newKeyDescription, setNewKeyDescription] = useState("");
  const [newlyCreatedKey, setNewlyCreatedKey] = useState(null);
  const [showNewKey, setShowNewKey] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    fetchApiKeys();
  }, []);

  const fetchApiKeys = async () => {
    try {
      const response = await axios.get(`${API}/auth/api-keys`);
      setApiKeys(response.data);
    } catch (error) {
      console.error("Failed to fetch API keys:", error);
      toast({
        title: "Error",
        description: "Failed to load API keys",
        variant: "destructive",
      });
    }
  };

  const createApiKey = async () => {
    if (!newKeyName.trim()) {
      toast({
        title: "Error",
        description: "Please enter a name for the API key",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API}/auth/api-keys`, {
        name: newKeyName,
        description: newKeyDescription
      });

      setNewlyCreatedKey(response.data);
      setShowCreateDialog(false);
      setNewKeyName("");
      setNewKeyDescription("");
      await fetchApiKeys();

      toast({
        title: "Success",
        description: "API key created successfully",
      });
    } catch (error) {
      console.error("Failed to create API key:", error);
      toast({
        title: "Error",
        description: error.response?.data?.detail || "Failed to create API key",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const revokeApiKey = async (keyId, keyName) => {
    if (!window.confirm(`Are you sure you want to revoke the API key "${keyName}"? This action cannot be undone.`)) {
      return;
    }

    try {
      await axios.delete(`${API}/auth/api-keys/${keyId}`);
      await fetchApiKeys();
      toast({
        title: "Success",
        description: "API key revoked successfully",
      });
    } catch (error) {
      console.error("Failed to revoke API key:", error);
      toast({
        title: "Error",
        description: "Failed to revoke API key",
        variant: "destructive",
      });
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied",
      description: "API key copied to clipboard",
    });
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <Card className="bg-slate-900 border-slate-800">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Key className="w-5 h-5 text-purple-400" />
            <CardTitle className="text-white">API Keys</CardTitle>
          </div>
          <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
            <DialogTrigger asChild>
              <Button className="bg-purple-600 hover:bg-purple-700">
                <Plus className="w-4 h-4 mr-2" />
                Create API Key
              </Button>
            </DialogTrigger>
            <DialogContent className="bg-slate-900 border-slate-800">
              <DialogHeader>
                <DialogTitle className="text-white">Create New API Key</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="keyName" className="text-gray-300">
                    Name
                  </Label>
                  <Input
                    id="keyName"
                    value={newKeyName}
                    onChange={(e) => setNewKeyName(e.target.value)}
                    placeholder="e.g., Mobile App, Webhook Integration"
                    className="bg-slate-800 border-slate-700 text-white"
                  />
                </div>
                <div>
                  <Label htmlFor="keyDescription" className="text-gray-300">
                    Description (optional)
                  </Label>
                  <Input
                    id="keyDescription"
                    value={newKeyDescription}
                    onChange={(e) => setNewKeyDescription(e.target.value)}
                    placeholder="What will this key be used for?"
                    className="bg-slate-800 border-slate-700 text-white"
                  />
                </div>
                <div className="flex justify-end space-x-2">
                  <Button
                    variant="outline"
                    onClick={() => setShowCreateDialog(false)}
                    className="border-slate-700 text-gray-300"
                  >
                    Cancel
                  </Button>
                  <Button
                    onClick={createApiKey}
                    disabled={loading}
                    className="bg-purple-600 hover:bg-purple-700"
                  >
                    {loading ? "Creating..." : "Create Key"}
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </CardHeader>
      <CardContent>
        {newlyCreatedKey && (
          <div className="mb-6 p-4 bg-green-900/20 border border-green-800 rounded-lg">
            <h3 className="text-green-400 font-medium mb-2">API Key Created Successfully!</h3>
            <p className="text-gray-300 text-sm mb-3">
              Please copy this key now. You won't be able to see it again.
            </p>
            <div className="flex items-center space-x-2">
              <Input
                value={newlyCreatedKey.key}
                readOnly
                type={showNewKey ? "text" : "password"}
                className="bg-slate-800 border-slate-700 text-white font-mono text-sm"
              />
              <Button
                size="sm"
                variant="outline"
                onClick={() => setShowNewKey(!showNewKey)}
                className="border-slate-700"
              >
                {showNewKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </Button>
              <Button
                size="sm"
                onClick={() => copyToClipboard(newlyCreatedKey.key)}
                className="bg-green-600 hover:bg-green-700"
              >
                <Copy className="w-4 h-4" />
              </Button>
            </div>
            <Button
              size="sm"
              variant="outline"
              onClick={() => setNewlyCreatedKey(null)}
              className="mt-3 border-slate-700 text-gray-300"
            >
              Dismiss
            </Button>
          </div>
        )}

        {apiKeys.length === 0 ? (
          <div className="text-center py-8">
            <Key className="w-12 h-12 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400">No API keys created yet</p>
            <p className="text-gray-500 text-sm">Create your first API key to start integrating with external applications</p>
          </div>
        ) : (
          <div className="space-y-3">
            {apiKeys.map((key) => (
              <div
                key={key.id}
                className="flex items-center justify-between p-4 bg-slate-800 rounded-lg border border-slate-700"
              >
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <h3 className="text-white font-medium">{key.name}</h3>
                    <span className="text-xs text-gray-400 font-mono bg-slate-700 px-2 py-1 rounded">
                      {key.key_preview}
                    </span>
                  </div>
                  {key.description && (
                    <p className="text-gray-400 text-sm mt-1">{key.description}</p>
                  )}
                  <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                    <span>Created: {formatDate(key.created_at)}</span>
                    {key.last_used && (
                      <span>Last used: {formatDate(key.last_used)}</span>
                    )}
                  </div>
                </div>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => revokeApiKey(key.id, key.name)}
                  className="border-red-800 text-red-400 hover:bg-red-900/20"
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            ))}
          </div>
        )}

        <div className="mt-6 p-4 bg-slate-800 rounded-lg">
          <h3 className="text-white font-medium mb-2">Using API Keys</h3>
          <p className="text-gray-400 text-sm mb-2">
            Include your API key in the request header:
          </p>
          <code className="block bg-slate-700 p-2 rounded text-xs text-gray-300 font-mono">
            X-API-Key: your-api-key-here
          </code>
        </div>
      </CardContent>
    </Card>
  );
};

export default ApiKeyManager;
