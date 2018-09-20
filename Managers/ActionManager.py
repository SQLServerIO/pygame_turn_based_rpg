from Managers.Manager import Manager, ACTION_MANAGER
from Shared import Rolls
from Shared.Action import Attack, RangeAttack, Skip
from Shared.GameConstants import GameConstants
from Shared.Skill import Skill
from Shared.Spell import Spell
import logging
logger = logging.getLogger().getChild(__name__)


""" Key (model_ws) : value (dict : key (enemy_ws) : value (dice roll to hit)) """
# rows: model's weapon skill, columns: target's weapon skill
TO_HIT_CHART_CLOSE_COMBAT = {
    1: {1: 4, 2: 4, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5},
    2: {1: 3, 2: 4, 3: 4, 4: 4, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5},
    3: {1: 3, 2: 3, 3: 4, 4: 4, 5: 4, 6: 4, 7: 5, 8: 5, 9: 5, 10: 5},
    4: {1: 3, 2: 3, 3: 3, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4, 9: 5, 10: 5},
    5: {1: 3, 2: 3, 3: 3, 4: 3, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4},
    6: {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4},
    7: {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 4, 8: 4, 9: 4, 10: 4},
    8: {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 4, 9: 4, 10: 4},
    9: {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 4, 10: 4},
    10: {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3, 10: 4},
}

TO_HIT_CHART_RANGED = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 0, 8: -1, 9: -2, 10: -3}

# rows: model's strength, columns: target_toughness
TO_WOUND_CHART = {
    1: {1: 4, 2: 5, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6},
    2: {1: 3, 2: 4, 3: 5, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6},
    3: {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6},
    4: {1: 2, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 6, 8: 6, 9: 6, 10: 6},
    5: {1: 2, 2: 2, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 6, 9: 6, 10: 6},
    6: {1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 6, 10: 6},
    7: {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 6},
    8: {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 3, 8: 4, 9: 5, 10: 6},
    9: {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 3, 9: 4, 10: 5},
    10: {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 3, 10: 4},
}

# keys are the attacking model's strength
ARMOR_SAVE_MODIFIER = {1: 0, 2: 0, 3: 0, 4: -1, 5: -2, 6: -3, 7: -4, 8: -5, 9: -6, 10: -7}


def is_double_damage(model, weapon, target):

    flaming_attack = False
    flammable = False

    for sr in model.get_special_rules_list():
        if sr.is_flaming_attack():
            flaming_attack = True

    for sr in weapon.get_special_rules_list():
        if sr.is_flaming_attack():
            flaming_attack = True

    for sr in target.get_special_rules_list():
        if sr.is_flammable():
            flammable = True

    if flaming_attack and flammable:
        return True


class ActionManager(Manager):

    def __init__(self, scene):
        super(ActionManager, self).__init__(scene, ACTION_MANAGER)
        logger.info("Init")

    def get_current_model(self):
        return self.get_turn_manager().get_current_model()

    def perform_action(self, model):

        action = model.get_action()
        logger.info("{} performing action:".format(model.get_name()))

        if isinstance(action, Attack):
            self.__close_combat_attacks(model)
        elif isinstance(action, RangeAttack):
            self.__range_attack(model)
        elif isinstance(action, Skill):
            self.__skill(model)
        elif isinstance(action, Spell):
            self.__cast(model)
        elif isinstance(action, Skip):
            model.set_action_done()

        """ Model set action done"""
        model.set_action_done()  # mark models action as done

    def wound_target(self, target, strength=4, armor_saves_allowed=False, double_effect=False):
        target.set_animation("hurt")
        logger.info("Rolling to wound:")
        roll = Rolls.get_d6_roll()
        if roll == 6:
            logger.info("Target wounded!")
        elif roll == 1:
            logger.info("Failed to wound target!")
            self.__add_text_blocked(target)
            return
        else:
            toughness = target.get_toughness()
            required_roll = TO_WOUND_CHART[strength][toughness]
            logger.info("Required roll to wound: " + str(required_roll))
            if roll >= required_roll:
                logger.info("Target wounded!")
            else:
                logger.info("Failed to wound target!")
                self.__add_text_blocked(target)
                return

        if armor_saves_allowed:
            logger.info("Target rolling to armor save:")
            roll = Rolls.get_d6_roll()
            if roll == 1:
                logger.info("Target armor save throw failed")
            else:
                target_armor = target.get_armor()
                target_shield = target.get_shield()

                if target_armor is None:
                    armor_req_roll = 7
                else:
                    armor_req_roll = target_armor.get_required_roll()

                if target_shield is None:
                    shield_save_modifier = 0
                else:
                    shield_save_modifier = target_shield.get_shield_save_modifier()

                # the required target roll to be saved by the armor
                required_roll = armor_req_roll + shield_save_modifier

                required_roll -= ARMOR_SAVE_MODIFIER[strength]  # Model/Weapon strength negates the armor save
                logger.info("Required roll for armor save: " + str(required_roll))

                if roll >= required_roll:
                    logger.info("Target armor save throw failed")
                    self.__add_text_blocked(target)
                    return

        # saved_by_ward = self.__get_ward_saving_throw(target)
        saved_by_ward = self.__get_ward_saving_throw()
        if saved_by_ward:
            logger.info("Target saved by ward!")
            self.__add_text_saved_by_ward(target)
            return

        target_wounds = target.get_current_wounds()
        if double_effect:
            logger.info("Double damage!")
            wounds = 2
        else:
            wounds = 1
        self.__add_text_hit(target)
        target.set_wounds(target_wounds - wounds)
        return

    # def get_turn_manager(self):
    #     return self.__scene.get_turn_manager()

    def __close_combat_attacks(self, model):
        current_model = model
        logger.info("{}: Close Combat".format(current_model.get_name()))
        targets = current_model.get_targets()
        if type(targets) is not list:
            targets = [targets]
        number_of_attacks = current_model.get_attacks()
        for a in range(number_of_attacks):

            alive_targets = [x for x in targets if not x.is_killed()]

            if not any(alive_targets):
                logger.info("No targets alive!")
                return
            logger.info("---------- ATTACK#{}/{} ----------".format(str(a+1), str(number_of_attacks)))

            logger.info("{}: setting animation to attack".format(current_model.get_name()))
            current_model.set_animation("attack")

            target = alive_targets[0]  # get the first remaining alive target
            logger.info("{}: setting target ({}) animation to hurt".format(current_model.get_name(), target.get_name()))
            target.set_animation("hurt")

            hit = self.__get_roll_to_hit_close_combat(target)
            if not hit:
                # look for any re-roll to hit special rule the model has
                for sr in current_model.get_special_rules_list():
                    if sr.re_roll_to_hit(target):
                        hit = self.__get_roll_to_hit_close_combat(target)
                        if hit:
                            logger.info("Successfully re-rolled to hit with: {}".format(sr.get_name()))
                            break
            if hit:
                wound, killing_blow = self.__get_roll_to_wound(target)
                if not wound:
                    # look for an re-roll to wound special rule the model has
                    for sr in current_model.get_special_rules_list():
                        if sr.re_roll_to_wound(target, Attack):
                            wound, killing_blow = self.__get_roll_to_wound(target)
                            if wound:
                                logger.info("Successfully re-rolled to wound with: {}".format(sr.get_name()))
                                break
                if wound and killing_blow:
                    # saved_by_ward = self.get_ward_saving_throw(target)
                    saved_by_ward = False
                    if saved_by_ward:
                        self.__add_text_saved_by_ward(target)
                        continue
                    else:
                        target.set_wounds(0)
                        self.__add_text("Killing Blow!", GameConstants.BRIGHT_RED, target)
                elif wound:
                    saved_by_armor = self.__get_armor_saving_throw(target)
                    if not saved_by_armor:
                        # TODO: return the wards
                        # saved_by_ward = self.get_ward_saving_throw(target)
                        saved_by_ward = False
                        if saved_by_ward:
                            self.__add_text_saved_by_ward(target)
                            continue
                        else:
                            self.__add_text_hit(target)
                            target_wounds = target.get_current_wounds()
                            weapon = current_model.get_melee_weapon()
                            double_damage = is_double_damage(current_model, weapon, target)
                            if double_damage:
                                target.set_wounds(target_wounds - 2)
                            else:
                                target.set_wounds(target_wounds - 1)

                    else:
                        self.__add_text_blocked(target)
                else:
                    self.__add_text_blocked(target)
            else:
                self.__add_text_miss(target)

    def __range_attack(self, model):
        current_model = model
        logger.info("{}: Range Attack".format(current_model.get_name()))
        targets = current_model.get_targets()
        if type(targets) is not list:
            targets = [targets]

        alive_targets = [x for x in targets if not x.is_killed()]

        if not any(alive_targets):
            logger.info("No targets alive!")
            return

        logger.info("---------- RANGE ATTACK ----------")
        logger.info("{}: setting animation to shoot".format(current_model.get_name()))
        current_model.set_animation("shoot")

        target = alive_targets[0]  # 1st target
        logger.info("{}: setting target ({}) animation to hurt".format(current_model.get_name(), target.get_name()))
        target.set_animation("hurt")

        hit = self.__get_roll_to_hit_ranged(target)
        if hit:
            wound, killing_blow = self.__get_roll_to_wound(target)
            if wound and killing_blow:
                # saved_by_ward = self.__get_ward_saving_throw(target)
                saved_by_ward = self.__get_ward_saving_throw()
                if saved_by_ward:
                    return
                else:
                    # killing blow ignores any armor save BUT NOT WARD SAVES
                    target.set_wounds(0)
                    self.__add_text("Killing Blow!", GameConstants.BRIGHT_RED, target)
            elif wound:
                saved_by_armor = self.__get_armor_saving_throw(target)
                if not saved_by_armor:
                    # saved_by_ward = self.get_ward_saving_throw(target)
                    # if saved_by_ward:
                    #     return
                    # else:
                    self.__add_text_hit(target)
                    target_wounds = target.get_wounds()
                    weapon = current_model.get_ranged_weapon()
                    double_damage = is_double_damage(current_model, weapon, target)
                    if double_damage:
                        target.set_wounds(target_wounds - 2)
                    else:
                        target.set_wounds(target_wounds - 1)
                else:
                    self.__add_text_blocked(target)
            else:
                self.__add_text_blocked(target)
        else:
            self.__add_text_miss(target)

    def __skill(self, model):

        current_model = model
        skill = current_model.get_action()
        logger.info("{}: Use {}".format(current_model.get_name(), skill.get_name()))
        logger.info("{}: setting animation to cast".format(current_model.get_name()))
        current_model.set_animation("cast")

        self.__add_text(string=skill.get_name(), text_color=GameConstants.CYAN, target=current_model)
        skill.on_click(self)

    def __cast(self, model):
        current_model = model
        spell = current_model.get_action()
        logger.info("{}: Use {}".format(current_model.get_name(), spell.get_name()))
        logger.info("{}: setting animation to cast".format(current_model.get_name()))
        current_model.set_animation("cast")

        self.__add_text(string=spell.get_name(), text_color=GameConstants.CYAN, target=current_model)
        cast_successful = spell.on_click(self)
        if not cast_successful:
            self.__add_text_miscast(current_model)
            current_model.set_miscast()

    def __get_roll_to_hit_close_combat(self, target) -> bool:
        logger.info("Rolling to hit:")
        roll = Rolls.get_d6_roll()
        if roll == 6:
            logger.info("Target hit!")
            return True
        elif roll == 1:
            logger.info("Missed target!")
            return False
        else:
            current_model = self.get_current_model()
            ws = current_model.get_weapon_skill()
            target_ws = target.get_weapon_skill()
            required_roll = TO_HIT_CHART_CLOSE_COMBAT[ws][target_ws]
            logger.info("Required roll to hit: " + str(required_roll))
            if roll >= required_roll:
                logger.info("Target hit!")
                return True
        logger.info("Missed target!")
        return False

    # noinspection PyUnusedLocal
    def __get_roll_to_hit_ranged(self, target) -> bool:
        # TODO: target might be behind cover
        logger.info("Rolling to hit:")
        roll = Rolls.get_d6_roll()
        if roll == 6:
            logger.info("Target hit!")
            return True
        elif roll == 1:
            logger.info("Missed target!")
            return False
        else:
            current_model = self.get_current_model()
            bs = current_model.get_ballistic_skill()
            required_roll = TO_HIT_CHART_RANGED[bs]
            logger.info("Required roll to hit: " + str(required_roll))
            if roll >= required_roll:
                logger.info("Target hit!")
                return True
        logger.info("Missed target!")
        return False

    def __get_roll_to_wound(self, target) -> (bool, bool):
        logger.info("Rolling to wound:")
        current_model = self.get_current_model()
        roll = Rolls.get_d6_roll()
        if roll == 6:
            logger.info("Target wounded!")
            for sr in current_model.get_special_rules_list():
                if sr.is_killing_blow(target):
                    logger.info("Killing Blow!")
                    return True, True
            return True, False
        elif roll == 1:
            logger.info("Failed to wound target!")
            return False, False
        else:
            s = current_model.get_strength()
            for sr in current_model.get_special_rules_list():
                # get any strength bonus special rule the model has
                s += sr.get_strength_bonus()
            target_t = target.get_toughness()
            required_roll = TO_WOUND_CHART[s][target_t]
            logger.info("Required roll to wound: " + str(required_roll))
            if roll >= required_roll:
                logger.info("Target wounded!")
                return True, False
        logger.info("Failed to wound target!")
        return False, False

    def __get_armor_saving_throw(self, target) -> bool:
        logger.info("Target rolling to armor save:")
        roll = Rolls.get_d6_roll()
        if roll == 1:
            logger.info("Target armor save throw failed")
            return False
        else:
            current_model = self.get_current_model()
            s = current_model.get_strength()
            target_armor = target.get_armor()
            target_shield = target.get_shield()

            if target_armor is None:
                armor_req_roll = 7
            else:
                armor_req_roll = target_armor.get_required_roll()

            if target_shield is None:
                shield_save_modifier = 0
            else:
                shield_save_modifier = target_shield.get_shield_save_modifier()

            # the required target roll to be saved by the armor
            required_roll = armor_req_roll + shield_save_modifier

            required_roll -= ARMOR_SAVE_MODIFIER[s]  # Model/Weapon strength negates the armor save
            logger.info("Required roll for armor save: " + str(required_roll))

            if roll >= required_roll:
                return True
        logger.info("Target armor save throw failed")
        return False

    # noinspection PyMethodMayBeStatic
    # def __get_ward_saving_throw(self, target) -> bool:
    def __get_ward_saving_throw(self) -> bool:
        logger.info("Target rolling to ward save:")

        # TODO: finish ward saving throw
        logger.info("Incomplete code!")
        return False

        # roll = Rolls.get_d6_roll()
        # if roll == 1:
        #     logger.info("Target save throw failed")
        #     return False
        # else:
        #     target_wards = target.get_wards()  # always roll on the best ward, they don't accumulate
        #     # TODO: wards should be objects
        #     for ward in target_wards:
        #         if "ARMOR" in ward or "SHIELD" in ward or "TALISMAN" in ward:
        #
        #             if Bestiary.WARD_SHIELD_CHARMED in ward:
        #                 # charmed shield is single use only
        #                 target.remove_ward(ward)
        #
        #             required_roll = WARD_SAVES[ward]
        #             if roll >= required_roll:
        #                 logger.info("Target saved by armor!")
        #                 return True
        #
        # logger.info("Target save throw failed")
        # return False

    # -------- Texts -------- #
    # noinspection PyMethodMayBeStatic
    def __add_text(self, string, text_color, target):
        target.add_action_results_text(string, text_color)

    def __add_text_miss(self, target):
        self.__add_text("Miss", GameConstants.BRIGHT_YELLOW, target)

    def __add_text_hit(self, target):
        self.__add_text("Hit", GameConstants.BRIGHT_YELLOW, target)

    def __add_text_blocked(self, target):
        self.__add_text("Blocked", GameConstants.BRIGHT_YELLOW, target)

    def __add_text_saved_by_ward(self, target):
        self.__add_text("Saved by ward", GameConstants.BRIGHT_YELLOW, target)

    def __add_text_miscast(self, target):
        self.__add_text("Miscast!", GameConstants.BRIGHT_YELLOW, target)
