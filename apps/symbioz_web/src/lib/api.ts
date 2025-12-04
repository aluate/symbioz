/**
 * API client for Symbioz game backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002';

export interface Character {
  name: string;
  race: string;
  class: string;
  level: number;
  hp: number;
  maxHp: number;
  xp: number;
  credits: number;
  attributes: {
    STR: number;
    DEX: number;
    CON: number;
    INT: number;
    WIS: number;
    CHA: number;
  };
  weapon: string | null;
  armor: string | null;
  inventory: string[];
  abilities: string[];
  status_effects: string[];
}

export interface Enemy {
  name: string;
  level: number;
  hp: number;
  maxHp: number;
  attributes: Record<string, number>;
}

export interface CombatState {
  player: Character;
  enemies: Enemy[];
  round: number;
  is_player_turn: boolean;
  current_actor: string | null;
}

export interface Mission {
  id: number;
  name: string;
  description: string;
  type: string;
  xp_reward: number;
}

export interface Race {
  id: number;
  name: string;
  description: string;
}

export interface Class {
  id: number;
  name: string;
  description: string;
  abilities: string[];
}

class ApiClient {
  private sessionId: string | null = null;

  async createSession(): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/api/session/create`, {
      method: 'POST',
    });
    const data = await response.json();
    this.sessionId = data.session_id;
    localStorage.setItem('symbioz_session_id', this.sessionId);
    return this.sessionId;
  }

  getSessionId(): string | null {
    if (!this.sessionId) {
      this.sessionId = localStorage.getItem('symbioz_session_id');
    }
    return this.sessionId;
  }

  async ensureSession(): Promise<string> {
    let sessionId = this.getSessionId();
    if (!sessionId) {
      sessionId = await this.createSession();
    }
    return sessionId;
  }

  async createCharacter(name: string, raceId: number, classId: number): Promise<Character> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/character/create?session_id=${sessionId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, race_id: raceId, class_id: classId }),
    });
    const data = await response.json();
    if (data.session_id) {
      this.sessionId = data.session_id;
      localStorage.setItem('symbioz_session_id', this.sessionId);
    }
    return data.character;
  }

  async getCharacter(): Promise<Character> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/character?session_id=${sessionId}`);
    const data = await response.json();
    return data;
  }

  async getRaces(): Promise<Race[]> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/races?session_id=${sessionId}`);
    const data = await response.json();
    return data.races;
  }

  async getClasses(): Promise<Class[]> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/classes?session_id=${sessionId}`);
    const data = await response.json();
    return data.classes;
  }

  async getMissions(): Promise<Mission[]> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/missions?session_id=${sessionId}`);
    const data = await response.json();
    return data.missions;
  }

  async startMission(missionId: number): Promise<any> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/mission/start?session_id=${sessionId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mission_id: missionId }),
    });
    return await response.json();
  }

  async getCombatState(): Promise<CombatState> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/combat/state?session_id=${sessionId}`);
    const data = await response.json();
    return data;
  }

  async combatAction(
    actionType: string,
    targetId?: number,
    abilityName?: string,
    itemName?: string
  ): Promise<any> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/combat/action?session_id=${sessionId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action_type: actionType,
        target_id: targetId,
        ability_name: abilityName,
        item_name: itemName,
      }),
    });
    return await response.json();
  }

  async rest(): Promise<Character> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/hub/rest?session_id=${sessionId}`, {
      method: 'POST',
    });
    const data = await response.json();
    return data.character;
  }

  async getVendorItems(): Promise<{ items: any[]; player_credits: number }> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/hub/vendor?session_id=${sessionId}`);
    const data = await response.json();
    return data;
  }

  async purchaseItem(itemId: number): Promise<Character> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/hub/vendor/purchase?session_id=${sessionId}&item_id=${itemId}`, {
      method: 'POST',
    });
    const data = await response.json();
    return data.character;
  }

  async skillCheck(attribute: string, dc: number): Promise<any> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/skill/check?session_id=${sessionId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ attribute, dc }),
    });
    return await response.json();
  }

  async completeSkillMission(success: boolean): Promise<any> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/skill/complete?session_id=${sessionId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success }),
    });
    return await response.json();
  }

  async saveGame(): Promise<void> {
    const sessionId = await this.ensureSession();
    await fetch(`${API_BASE_URL}/api/session/save?session_id=${sessionId}`, {
      method: 'POST',
    });
  }

  async loadGame(): Promise<boolean> {
    const sessionId = await this.ensureSession();
    const response = await fetch(`${API_BASE_URL}/api/session/load?session_id=${sessionId}`);
    const data = await response.json();
    return data.has_character || false;
  }
}

export const api = new ApiClient();

